"""Opt-in native acceptance tests. Creates/closes ONLY disposable project tabs.

Run with --output-root OUTSIDE the skill/repository. Requires saved live projects.
Never recalculates or saves any project that was open when testing started.
"""
import argparse
import json
from pathlib import Path
import time
from msproject_native import attach,export,run,iso,native_evidence
from guardian import audit,compare_protected,child

def make(app,folder,kind='fs'):
    app.FileNew();owned=app.ActiveProject
    try:
        owned.ProjectStart='11/2/2026 8:00 AM'
        tasks=[]
        for name,duration in [('Mobilize and rough in','4d'),('Inspection','2d'),('Completion','0d')]:
            t=owned.Tasks.Add(name);t.Manual=False;t.Duration=app.DurationValue(duration);tasks.append(t)
        a,b,c=tasks
        if kind=='overlap':
            b.Duration=app.DurationValue('6d');b.TaskDependencies.Add(a,3,'1d');c.TaskDependencies.Add(b,0,'0d')
        else:b.TaskDependencies.Add(a,1,'1d' if kind=='calendar' else '0d');c.TaskDependencies.Add(b,1,'0d')
        if kind=='calendar':
            # Explicit project holiday and a separate successor task-calendar exception.
            cal=owned.Calendar
            cal.Exceptions.Add(Type=1,Name='Project holiday',Start='11/6/2026',Finish='11/6/2026')
            app.BaseCalendarCreate(Name='Inspection exception',FromName=cal.Name)
            taskcal=owned.BaseCalendars.Item('Inspection exception')
            taskcal.Exceptions.Add(Type=1,Name='Inspection unavailable',Start='11/10/2026',Finish='11/10/2026')
            b.Calendar=taskcal.Name
        if kind=='actual':b.ActualStart='11/2/2026 8:00 AM'
        if kind=='manual':b.Manual=True;b.Start='11/2/2026 8:00 AM';b.Finish='11/3/2026 5:00 PM'
        if kind=='hard':b.ConstraintType=3;b.ConstraintDate='11/3/2026 5:00 PM'
        if not app.CalculateProject():raise RuntimeError('Fixture recalculation failed')
        uids=[str(t.UniqueID) for t in tasks]
        policy={'completion_uid':uids[2],'open_end_exceptions':{uids[0]:{'predecessor':'Project start'},uids[2]:{'successor':'Completion milestone'}}}
        path=folder/(kind+'.mpp')
        app.FileSaveAs(Name=str(path),FormatID='MSProject.mpp')
        return path,policy,uids
    finally:app.FileClose(0)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output-root',required=True)
    p.add_argument('--interactive-conflicts',action='store_true',help='Opt into a test that can block on a Project Planning Wizard dialog')
    args=p.parse_args()
    folder=Path(args.output_root)/('native-tests-'+str(time.time_ns()));folder.mkdir(parents=True)
    app=attach();original=[(p.Name,str(p.FullName),bool(p.Saved)) for p in app.Projects]
    if any(not x[2] for x in original):raise RuntimeError('Save open projects before native tests')
    results=[]
    def persist():
        (folder/'acceptance-results.json').write_text(json.dumps({'results':results,
            'all_passed':bool(results) and all(x.get('passed') is True for x in results),
            'case_6':'Run test_guardian.py: corrupt graph fixtures are audited offline'},indent=2),encoding='utf-8')
    def check(name,func):
        try:detail=func();results.append({'case':name,'passed':True,'detail':detail});print('PASS',name,flush=True)
        except Exception as e:results.append({'case':name,'passed':False,'error':str(e)});print('FAIL',name,str(e)[:300],flush=True)
        persist()
    path,policy,uids=make(app,folder)
    def execute(intent,**kw):return run(path,folder,policy,{'uid':uids[1],'intent':intent,**kw})
    def feasible():
        r=execute('exact_finish',date='2026-11-10');assert r['status']=='PASS',r
        assert r['saved_reopened_verified'] and r['original_bytes_preserved'];return r['run_directory']
    check('1 feasible finish preserves every dependency',feasible)
    def impossible():
        r=execute('exact_finish',date='2026-11-03');assert r['status']=='FAIL' and not r['applied'] and r['blocking_chain'],r
        assert r['before']==r['after'];return r['native_forecast_under_retained_inputs']
    check('2 impossible earlier finish reports blocking network',impossible)
    def delay():
        r=run(path,folder,policy,{'uid':uids[0],'intent':'duration','duration':'6d'});assert r['status']=='PASS',r
        assert r['after'][uids[1]]['Start']>r['before'][uids[1]]['Start'];return r['run_directory']
    check('3 delayed predecessor moves successors',delay)
    def overlap():
        path2,pol,ids=make(app,folder,'overlap');r=run(path2,folder,pol,{'uid':ids[1],'intent':'target','date':'2026-12-01'})
        assert r['status']=='PASS',r
        assert r['after'][ids[1]]['Start']<r['after'][ids[0]]['Finish'];return r['run_directory']
    check('4 SS and FF permit overlap',overlap)
    def calendar():
        path2,pol,ids=make(app,folder,'calendar');r=run(path2,folder,pol,{'uid':ids[1],'intent':'target','date':'2026-12-01'})
        assert r['status']=='PASS',r
        assert r['after'][ids[1]]['Start'].startswith('2026-11-11'),r['after']
        return r['run_directory']
    check('5 lag weekend holiday task-calendar exception',calendar)
    def actual():
        path2,pol,ids=make(app,folder,'actual');r=run(path2,folder,pol,{'uid':ids[1],'intent':'target','date':'2026-12-01'})
        assert 'OUT_OF_SEQUENCE_ACTUAL' in {f['code'] for f in r.get('after_audit',[])},r
        assert r['before'][ids[1]]['ActualStart']==r['after'][ids[1]]['ActualStart'];return r['status']
    check('7 actual conflict flagged and history preserved',actual)
    def masked():
        statuses=[]
        for kind in ('manual','hard'):
            path2,pol,ids=make(app,folder,kind);r=run(path2,folder,pol,{'uid':ids[1],'intent':'target','date':'2026-12-01'})
            codes={f['code'] for f in r.get('after_audit',[])}
            assert ('MANUAL' if kind=='manual' else 'HARD_CONSTRAINT') in codes,r
            assert r['status']!='PASS',r;statuses.append(r['status'])
        return statuses
    if args.interactive_conflicts:
        check('8 manual and hard constraints expose masked conflict',masked)
    else:
        results.append({'case':'8 native masked conflict','passed':None,'status':'UNVERIFIED','reason':'Known Planning Wizard modal; opt-in interactive test only'})
        persist()
    def roundtrip():
        r=execute('deadline',date='2026-12-01');assert r['status']=='PASS' and r['saved_reopened_verified'],r
        return r['run_directory']
    check('9 native saved reopened identities links calendars constraints',roundtrip)
    def existing():
        path2=folder/'actual.mpp';pol=policy;r=run(path2,folder,pol,{'uid':uids[1],'intent':'deadline','date':'2026-11-01'})
        assert r['status']=='FAIL',r
        assert 'OUT_OF_SEQUENCE_ACTUAL' in {x['code'] for x in r['findings']['existing']},r
        assert 'MISSED_DEADLINE' in {x['code'] for x in r['findings']['new']},r
        return r['run_directory']
    check('10 preexisting versus introduced findings',existing)
    final=[(p.Name,str(p.FullName),bool(p.Saved)) for p in app.Projects]
    results.append({'case':'live projects unchanged and restored','passed':original==final})
    report={'results':results,'all_passed':all(x['passed'] for x in results),
        'case_6':'Run test_guardian.py: invalid cycles/missing refs are audited offline instead of loading corrupt schedules into Project'}
    (folder/'acceptance-results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(str(folder));return 0 if report['all_passed'] else 1
if __name__=='__main__':raise SystemExit(main())
