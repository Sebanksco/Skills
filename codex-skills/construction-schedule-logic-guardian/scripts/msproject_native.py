"""Microsoft Project desktop adapter. Requires Windows, Project and pywin32.

Always operates on an exclusive versioned copy. Never calls CalculateAll.
Date strings are local Project wall-clock time, not Python timezone conversions.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
from pathlib import Path
import shutil
import uuid
from guardian import Schedule, audit, child, compare_protected, deltas, digest, finding, verdict

def attach():
    import win32com.client
    return win32com.client.gencache.EnsureDispatch(win32com.client.GetActiveObject('MSProject.Application'))

def iso(value):
    # COM exposes Project wall-clock values tagged UTC; do not convert time zones.
    return value.strftime('%Y-%m-%dT%H:%M:%S') if hasattr(value,'strftime') else str(value)

def project_date(value, finish=False):
    parsed=dt.datetime.fromisoformat(value)
    if len(value)==10:parsed=parsed.replace(hour=17 if finish else 8)
    return parsed.strftime('%m/%d/%Y %H:%M')

def export(app,path):
    if not app.FileSaveAs(Name=str(path),FormatID='MSProject.XML'):
        raise RuntimeError('Native XML export did not succeed')
    if not Path(path).is_file():raise RuntimeError('Native XML export file missing')
    return Schedule(path)

def native_evidence(app,schedule):
    p=app.ActiveProject
    byuid={str(t.UniqueID):t for t in p.Tasks if t is not None}
    edges={};limitations=[]
    if p.Resources.Count:
        limitations.append('Resource calendars, leveling and assignment interactions require native Task Inspector review; adapter bounds cover resource-free tasks only')
    if child(schedule.root,'ScheduleFromStart','1')!='1':
        limitations.append('Backward scheduled project needs separate native earliest-date review')
    for uid,t in byuid.items():
        try:
            if t.SplitParts.Count>1:limitations.append(f'Task {uid}: split progress needs separate remaining-work verification')
        except Exception:
            limitations.append(f'Task {uid}: split-state verification unavailable')
    for link in schedule.links:
        a,b,kind,lag,fmt,external,_=link;key='|'.join(link)
        record={'verified':False}
        try:
            if external=='1':raise ValueError('External dependency source unavailable')
            ta,tb=byuid[a],byuid[b]
            if bool(ta.Manual) or bool(tb.Manual):raise ValueError('Manual task: native bound not certified')
            if ta.Assignments.Count or tb.Assignments.Count:raise ValueError('Resource-assigned endpoint needs Task Inspector review')
            if kind not in ('0','1','2','3'):raise ValueError('Unknown dependency type')
            endpoint=ta.Finish if kind in ('0','1') else ta.Start
            amount=int(lag)/10
            if amount:
                if fmt not in ('3','5','7','9','11'):
                    raise ValueError('Elapsed/percentage/unknown lag format not certified by this adapter')
                calname=str(tb.Calendar)
                calendar=p.Calendar if calname in ('None','NA','') else p.BaseCalendars.Item(calname)
                endpoint=app.DateAdd(project_date(iso(endpoint)),f'{amount:g}m',calendar)
            record={'verified':True,'minimum':iso(endpoint),'method':'Project.DateAdd using successor calendar; zero lag uses native endpoint'}
        except Exception as exc:record['reason']=str(exc)
        edges[key]=record
    if limitations:
        edges['__limitations__']={'reasons':limitations}
    return {'native_recalculated':True,'application':app.Name,'version':app.Version,'edges':edges,'limitations':limitations}

def upstream(schedule,uid):
    edges={u:[] for u in schedule.tasks}
    for a,b,*_ in schedule.links:
        if b in edges:edges[b].append(a)
    visited=set();stack=[str(uid)]
    while stack:
        u=stack.pop()
        if u in visited:continue
        visited.add(u);stack.extend(edges.get(u,[]))
    return [{'uid':u,**schedule.fields(u)} for u in sorted(visited) if u in schedule.tasks]

def apply_request(app,request):
    task=app.ActiveProject.Tasks.UniqueID(int(request['uid']))
    if task is None:raise ValueError('Requested stable UID is missing')
    intent=request['intent'];date=request.get('date')
    allowed={str(request['uid']):[]}
    if intent=='deadline':
        task.Deadline=project_date(date,True);allowed[str(task.UniqueID)]=['Deadline']
    elif intent=='exact_finish':
        task.ConstraintType=3;task.ConstraintDate=project_date(date,True)
        allowed[str(task.UniqueID)]=['ConstraintType','ConstraintDate']
    elif intent=='exact_start':
        task.ConstraintType=2;task.ConstraintDate=project_date(date)
        allowed[str(task.UniqueID)]=['ConstraintType','ConstraintDate']
    elif intent=='actual_finish':
        task.ActualFinish=project_date(date,True)
        allowed[str(task.UniqueID)]=['ActualFinish','ActualDuration','ActualWork','PercentComplete','RemainingDuration']
        if not request.get('allow_derived_actual_start'):
            # A finish may imply an actual start. Comparison will block that unapproved rewrite.
            pass
        else:allowed[str(task.UniqueID)].append('ActualStart')
    elif intent=='duration':
        task.Duration=app.DurationValue(request['duration'])
        allowed[str(task.UniqueID)]=['Duration','RemainingDuration']
    elif intent!='target':raise ValueError('Unsupported intent; clarify actual/exact/deadline/target')
    return allowed

def run(source,output_root,policy,request):
    source=Path(source).resolve();root=Path(output_root).resolve()
    if source.suffix.lower()!='.mpp':raise ValueError('Automated editing requires full MPP; use documented native roundtrip for other formats')
    if not source.is_file():raise FileNotFoundError(source)
    run_dir=root/('guardian-'+dt.datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8])
    run_dir.mkdir(parents=True,exist_ok=False)
    source_hash=digest(source)
    copy=run_dir/(source.stem+'-revised.mpp');shutil.copy2(source,copy)
    app=attach();old_project=app.ActiveProject.Name if app.Projects.Count else None
    old_alerts=app.DisplayAlerts
    initial_count=app.Projects.Count
    # Refuse unsaved/open same source; never capture stale disk state as the user's latest schedule.
    for p in app.Projects:
        if str(p.FullName).lower()==str(source).lower() and not p.Saved:
            raise RuntimeError('Source is open with unsaved edits; save it explicitly before copying')
    owned=False;report={'request':request,'interpretation':request['intent'],'source_hash':source_hash,
        'source':str(source),'run_directory':str(run_dir),'status':'UNVERIFIED','applied':False}
    try:
        app.DisplayAlerts=False
        app.FileOpenEx(Name=str(copy),ReadOnly=False)
        if str(app.ActiveProject.FullName).lower()!=str(copy).lower():raise RuntimeError('Work copy did not become active')
        owned=True
        if app.Projects.Count!=initial_count+1:raise RuntimeError('Could not establish exclusive work-copy project')
        raw=export(app,run_dir/'captured.xml')
        e_captured=native_evidence(app,raw)
        e_captured['native_recalculated']=False
        captured_findings=audit(raw,policy,e_captured)
        report['captured_audit']=captured_findings
        if not app.CalculateProject():raise RuntimeError('Native recalculation returned false')
        before=export(app,run_dir/'before.xml');e_before=native_evidence(app,before)
        before_findings=audit(before,policy,e_before)
        pre_changes=compare_protected(raw,before)
        if pre_changes:raise RuntimeError('Recalculation changed protected inputs before edit: '+str(pre_changes))
        uid=str(request['uid'])
        if uid not in before.tasks:raise ValueError('Requested stable task UID not found')
        intent=request['intent'];current=before.fields(uid)
        report['blocking_chain']=upstream(before,uid)
        report['native_forecast_under_retained_inputs']=current['Finish' if intent!='exact_start' else 'Start']
        blocked=False
        if intent in ('exact_finish','exact_start'):
            field='Finish' if intent=='exact_finish' else 'Start'
            target=project_date(request['date'],field=='Finish')
            target_iso=dt.datetime.strptime(target,'%m/%d/%Y %H:%M').isoformat()
            blocked=current[field]>target_iso
        if blocked:
            report.update(feasible=False,reason='Requested date precedes native forecast under retained network, durations, calendars and constraints',
                proposed_decisions=['Approve a later date, or identify specific scope/resource/duration/calendar/logic changes for a separate scenario'],applied=False)
            allowed={}
        else:
            allowed=apply_request(app,request)
        if not app.CalculateProject():raise RuntimeError('Native recalculation returned false')
        after=export(app,run_dir/'after.xml');e_after=native_evidence(app,after)
        after_findings=audit(after,policy,e_after)
        for msg in compare_protected(before,after,allowed):after_findings.append(finding('PROTECTED_CHANGE',[],msg))
        for msg in e_after['limitations']:after_findings.append(finding('ENGINE_SCOPE',[],msg,'UNVERIFIED'))
        revised=copy
        # MPP Save As to a new name regenerates GUIDs. Copy bytes first, then FileSave.
        if not app.FileSave():raise RuntimeError('Native MPP save failed')
        app.FileClose(0);owned=False
        app.FileOpenEx(Name=str(revised),ReadOnly=True)
        if str(app.ActiveProject.FullName).lower()!=str(revised).lower():raise RuntimeError('Reopened copy did not become active')
        owned=True
        reopened=export(app,run_dir/'reopened.xml');e_reopen=native_evidence(app,reopened)
        reopen_findings=audit(reopened,policy,e_reopen)
        roundtrip=compare_protected(after,reopened)
        dates_changed={u:(after.fields(u),reopened.fields(u)) for u in after.tasks if u in reopened.tasks and after.fields(u)!=reopened.fields(u)}
        for msg in roundtrip:after_findings.append(finding('ROUNDTRIP_LOSS',[],msg))
        if dates_changed:after_findings.append(finding('ROUNDTRIP_DATES',list(dates_changed),'Saved/reopened task fields differ'))
        after_findings+=deltas(after_findings,reopen_findings)['new']
        if digest(source)!=source_hash:after_findings.append(finding('SOURCE_CHANGED',[],'Original source bytes changed during run'))
        target_ok=True
        if intent in ('exact_start','exact_finish') and not blocked:
            endpoint='Start' if intent=='exact_start' else 'Finish'
            target_ok=reopened.fields(uid)[endpoint]==dt.datetime.strptime(project_date(request['date'],endpoint=='Finish'),'%m/%d/%Y %H:%M').isoformat()
        if intent in ('deadline','target'):
            target_ok=reopened.fields(uid)['Finish']<=dt.datetime.strptime(project_date(request['date'],True),'%m/%d/%Y %H:%M').isoformat()
        if intent=='actual_finish':
            target_ok=reopened.fields(uid)['ActualFinish']==dt.datetime.strptime(project_date(request['date'],True),'%m/%d/%Y %H:%M').isoformat()
        if not target_ok:after_findings.append(finding('REQUEST_NOT_MET',[uid],'Native schedule does not meet requested date'))
        report.update(feasible=not blocked and target_ok,applied=not blocked and intent!='target',revised_copy=str(revised),
            before_audit=captured_findings,recalculated_before_audit=before_findings,
            recalculation_findings_delta=deltas(captured_findings,before_findings),
            after_audit=after_findings,findings=deltas(captured_findings,after_findings),
            before={u:before.fields(u) for u in before.tasks},after={u:reopened.fields(u) for u in reopened.tasks},
            affected_tasks=[u for u in before.tasks if u in reopened.tasks and before.fields(u)!=reopened.fields(u)],
            saved_reopened_verified=not roundtrip and not dates_changed,
            completion_uid=str(policy.get('completion_uid','')),
            critical_before=[u for u,t in before.tasks.items() if child(t,'Critical')=='1'],
            critical_after=[u for u,t in reopened.tasks.items() if child(t,'Critical')=='1'],
            status=verdict(after_findings,not roundtrip and not dates_changed,not blocked and target_ok),
            change_log=[{'uid':uid,'intent':intent,'allowed_fields':allowed.get(uid,[]),'applied':not blocked and intent!='target'}])
        report['earliest_feasible_finish_note']='Native forecast under retained inputs; not a resource-optimization proof. Existing constraints/actuals may prevent a true earliest-date claim.'
        report['candidate_changed']=report['applied']
        report['applied']=bool(report['candidate_changed'] and report['status']=='PASS')
        report['date_met']=not blocked and target_ok
        if report['status']=='UNVERIFIED':report['feasible']=None
        elif report['status']=='FAIL':report['feasible']=False
        for name,data in [('captured-evidence.json',e_captured),('before-evidence.json',e_before),('after-evidence.json',e_after),('reopened-evidence.json',e_reopen)]:
            (run_dir/name).write_text(json.dumps(data,indent=2),encoding='utf-8')
    except Exception as exc:
        report.update(status='UNVERIFIED',error=str(exc),applied=False)
    finally:
        try:
            if owned and str(app.ActiveProject.FullName).lower()==str(copy).lower():app.FileClose(0)
            app.DisplayAlerts=old_alerts
            report['original_project_restored']=not old_project or bool(app.Projects.Count and app.ActiveProject.Name==old_project)
        except Exception as exc:
            report.update(status='UNVERIFIED',cleanup_error=str(exc),original_project_restored=False)
        report['original_bytes_preserved']=digest(source)==source_hash
        (run_dir/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source');p.add_argument('--output-root',required=True)
    p.add_argument('--policy',required=True);p.add_argument('--request',required=True);a=p.parse_args()
    read=lambda path:json.loads(Path(path).read_text(encoding='utf-8-sig'))
    report=run(a.source,a.output_root,read(a.policy),read(a.request))
    print(json.dumps({'status':report['status'],'run_directory':report['run_directory'],'error':report.get('error')},indent=2))
    return 0 if report['status']=='PASS' else 2
if __name__=='__main__':raise SystemExit(main())
