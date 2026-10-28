"""Fail-closed MSPDI structural audit. This module never schedules dates."""
from __future__ import annotations
import argparse
import collections
import datetime as dt
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

NS = {'p': 'http://schemas.microsoft.com/project'}
TYPES = {'0': 'FF', '1': 'FS', '2': 'SF', '3': 'SS'}

def child(e, name, default=''):
    return e.findtext('p:' + name, default, NS)

def canonical(e):
    """Namespace-independent XML content, including unknown fields and duplicates."""
    return [e.tag.split('}')[-1], (e.text or '').strip(), sorted(e.attrib.items()),
            [canonical(x) for x in e]]

def protected_timephased(e):
    # Type 1 is assignment remaining work, a native calculated forecast.
    # Preserve every other type, including unknown types, conservatively.
    return [canonical(x) for x in e.findall('p:TimephasedData',NS) if child(x,'Type')!='1']

def timestamp(value):
    try:
        return dt.datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return None

class Schedule:
    def __init__(self, path):
        self.path = str(path)
        self.root = ET.parse(path).getroot()
        if self.root.tag != '{' + NS['p'] + '}Project':
            raise ValueError('Expected full Microsoft Project XML (MSPDI), not a task table')
        self.rows = self.root.findall('p:Tasks/p:Task', NS)
        self.tasks = {child(t, 'UID'): t for t in self.rows if child(t, 'UID') != '0'}
        self.links = []
        for uid, t in self.tasks.items():
            for link in t.findall('p:PredecessorLink', NS):
                self.links.append((child(link, 'PredecessorUID'), uid,
                                   child(link, 'Type', '1'), child(link, 'LinkLag', '0'),
                                   child(link, 'LagFormat', '7'), child(link, 'CrossProject', '0'),
                                   child(link, 'CrossProjectName')))

    def fields(self, uid):
        t = self.tasks[str(uid)]
        return {k: child(t, k) for k in ('Name','GUID','Start','Finish','ActualStart','ActualFinish',
            'PercentComplete','RemainingDuration','TotalSlack','FreeSlack','Critical',
            'ConstraintType','ConstraintDate','Deadline','Manual','CalendarUID','Summary')}

    def signature(self):
        return {'uids': sorted(self.tasks), 'guid': {u: child(t, 'GUID') for u,t in self.tasks.items()},
                'links': sorted(self.links),
                'link_payloads': sorted([json.dumps([u,canonical(e)],sort_keys=True) for u,t in self.tasks.items()
                                         for e in t.findall('p:PredecessorLink',NS)]),
                'calendars': [canonical(e) for e in self.root.findall('p:Calendars', NS)],
                'resources': [canonical(e) for e in self.root.findall('p:Resources', NS)],
                'project_policy': {k: child(self.root,k) for k in ('CalendarUID','ScheduleFromStart',
                    'StartDate','MinutesPerDay','MinutesPerWeek','DefaultStartTime','DefaultFinishTime')},
                'protected_tasks': {u: {k: [canonical(x) for x in t.findall('p:'+k,NS)] for k in
                    ('Duration','ActualStart','ActualFinish','ActualDuration','ActualWork',
                     'PercentComplete','RemainingDuration','Baseline','CalendarUID','IgnoreResourceCalendar',
                     'Manual','ConstraintType','ConstraintDate','Deadline','Type','EffortDriven',
                     'Stop','Resume','TimephasedData','ExternalTask','ExtendedAttribute')}
                    | {e.tag.split('}')[-1]:[canonical(x) for x in t.findall('p:'+e.tag.split('}')[-1],NS)]
                       for e in t if e.tag.split('}')[-1].startswith('Actual')}
                    for u,t in self.tasks.items()},
                'summary_baselines': [canonical(e) for e in self.root.findall('p:Tasks/p:Task[p:UID="0"]/p:Baseline',NS)],
                'assignments': [{k:[canonical(x) for x in e.findall('p:'+k,NS)] for k in
                    ('UID','GUID','TaskUID','ResourceUID','Units','ActualStart','ActualFinish','ActualWork',
                     'ActualOvertimeWork','ActualCost','Baseline')} | {'protected_timephased':protected_timephased(e)}
                    for e in self.root.findall('p:Assignments/p:Assignment',NS)]}

def finding(code, tasks, message, severity='ERROR', identity=None):
    return {'code':code, 'tasks':list(map(str,tasks)), 'severity':severity, 'message':message,
            'identity':identity or (message if code in ('PROTECTED_CHANGE','ROUNDTRIP_LOSS','ENGINE_SCOPE') else code)}

def audit(schedule, policy=None, evidence=None):
    policy, evidence = policy or {}, evidence or {}
    out=[]; tasks=schedule.tasks
    add=lambda c,u,m,s='ERROR',identity=None:out.append(finding(c,u,m,s,identity))
    ids=[child(t,'UID') for t in schedule.rows]
    for u,n in collections.Counter(ids).items():
        if n>1: add('DUPLICATE_UID',[u],'Task identity is ambiguous')
    graph={u:[] for u in tasks}; reverse={u:[] for u in tasks}
    seen=set()
    for a,b,kind,lag,fmt,external,external_name in schedule.links:
        pair=(a,b,kind,lag,fmt,external,external_name)
        if pair in seen: add('DUPLICATE_LINK',[a,b],'Duplicate relationship')
        seen.add(pair)
        if external=='1':
            add('EXTERNAL_UNVERIFIED',[a,b],'External dependency requires its source schedule','UNVERIFIED');continue
        if a not in tasks or b not in tasks:
            add('MISSING_TASK',[a,b],'Relationship references a missing UID');continue
        if a==b: add('SELF_LINK',[a],'Task depends on itself')
        graph[a].append(b);reverse[b].append(a)
        if kind not in TYPES: add('UNKNOWN_LINK',[a,b],f'Unknown relationship type {kind}','UNVERIFIED')
        if child(tasks[a],'Summary')=='1' or child(tasks[b],'Summary')=='1':
            add('SUMMARY_LINK',[a,b],'Summary task relationship needs review','WARNING')
        try:
            amount=int(lag)
            if amount<0: add('LEAD',[a,b],f'Negative lag {lag}, format {fmt}','WARNING')
            if abs(amount)>int(policy.get('long_lag_tenths_minutes',24000)):
                add('LONG_LAG',[a,b],f'Long lag {lag}, format {fmt}; review intended waiting work','WARNING')
        except ValueError: add('LAG_UNVERIFIED',[a,b],'Unreadable lag','UNVERIFIED')
    # Tarjan SCC: nonrecursive reachability avoids recursion limits on large schedules.
    remaining={u:len(reverse[u]) for u in tasks}; queue=[u for u,n in remaining.items() if n==0]; done=set()
    while queue:
        u=queue.pop();done.add(u)
        for v in graph[u]:
            remaining[v]-=1
            if remaining[v]==0:queue.append(v)
    cyclic=set(tasks)-done
    if cyclic:
        # Report only vertices with a path back to themselves, not innocent successors.
        cycle_members=[]
        for u in cyclic:
            visited=set();stack=list(graph[u])
            while stack:
                v=stack.pop()
                if v==u:cycle_members.append(u);break
                if v not in visited:visited.add(v);stack.extend(graph[v])
        if cycle_members:add('CYCLE',sorted(cycle_members),'Circular predecessor network')
    completion=str(policy.get('completion_uid',''))
    reaches=set();stack=[completion] if completion in tasks else []
    while stack:
        u=stack.pop()
        if u in reaches:continue
        reaches.add(u);stack.extend(reverse[u])
    if completion not in tasks:add('COMPLETION_UNVERIFIED',[],'Specify intended completion milestone UID','UNVERIFIED')
    exceptions=policy.get('open_end_exceptions',{})
    for u,t in tasks.items():
        if child(t,'Summary')=='1':continue
        for key,edges in [('predecessor',reverse[u]),('successor',graph[u])]:
            reason=exceptions.get(u,{}).get(key,'')
            if not edges and not reason:add('OPEN_'+key.upper(),[u],f'Missing expected {key}; document a legitimate exception')
        if completion in tasks and u not in reaches:add('DISCONNECTED',[u,completion],'No dependency path to intended completion')
        if child(t,'Manual')=='1':add('MANUAL',[u],'Manual scheduling can mask conflicts; engine audit is incomplete','UNVERIFIED')
        if child(t,'ConstraintType','0') in ('2','3','5','7'):
            add('HARD_CONSTRAINT',[u],'Date constraint can mask dependency conflicts','WARNING')
        if child(t,'ExternalTask')=='1':add('EXTERNAL_TASK',[u],'External task source not verified','UNVERIFIED')
        try:
            if int(child(t,'TotalSlack','0'))<0:add('NEGATIVE_FLOAT',[u],'Negative total float')
        except ValueError:add('FLOAT_UNVERIFIED',[u],'Total float unreadable','UNVERIFIED')
        finish=timestamp(child(t,'Finish'));deadline=timestamp(child(t,'Deadline'))
        if finish and deadline and finish>deadline:add('MISSED_DEADLINE',[u],f'Finish {finish.isoformat()} exceeds deadline {deadline.isoformat()}')
    native_edges=evidence.get('edges',{})
    for link in schedule.links:
        a,b,kind,lag,fmt,external,_=link
        if a not in tasks or b not in tasks or external=='1':continue
        key='|'.join(link)
        bound=native_edges.get(key,{})
        if not bound.get('verified'):
            add('EDGE_UNVERIFIED',[a,b],bound.get('reason','No native working-time relationship bound'),'UNVERIFIED',key);continue
        actual=timestamp(child(tasks[b], 'Start' if kind in ('1','3') else 'Finish'))
        minimum=timestamp(bound.get('minimum'))
        if not actual or not minimum:
            add('EDGE_UNVERIFIED',[a,b],'Missing native bound or endpoint','UNVERIFIED',key);continue
        if actual<minimum:
            add('RELATIONSHIP_VIOLATION',[a,b],f'{TYPES.get(kind,kind)} lag {lag}/{fmt}: endpoint {actual.isoformat()} before native bound {minimum.isoformat()}',identity=key)
            endpoint=child(tasks[b], 'ActualStart' if kind in ('1','3') else 'ActualFinish')
            if timestamp(endpoint):add('OUT_OF_SEQUENCE_ACTUAL',[a,b],f'Recorded actual {endpoint} conflicts; preserve history and review remaining work',identity=key)
    # Construction rules are supplied from requirements; heuristics are review findings only.
    for rule in policy.get('required_sequences',[]):
        a,b=str(rule['before']),str(rule['after'])
        visited=set();stack=[a] if a in tasks else []
        while stack:
            u=stack.pop()
            if u in visited:continue
            visited.add(u);stack.extend(graph[u])
        if b not in visited:add('CONSTRUCTION_SEQUENCE',[a,b],rule['reason'])
        else:
            add('CONSTRUCTION_REQUIREMENT_UNVERIFIED',[a,b],
                rule['reason']+'; graph reachability does not prove required timing, overlap or curing interval',
                'UNVERIFIED',json.dumps(rule,sort_keys=True))
    for u,t in tasks.items():
        if any(word in child(t,'Name').lower() for word in ('conceal','drywall','curing','commission','occupancy','load concrete')):
            add('CONSTRUCTION_REVIEW',[u],'Review inspection-before-concealment, curing/loading and commissioning/occupancy prerequisites against project requirements','WARNING')
    if not evidence.get('native_recalculated'):add('ENGINE_UNVERIFIED',[],'Native recalculation not proven','UNVERIFIED')
    return out

def compare_protected(before, after, allowed=None):
    """Only exact UID/field permissions permit changes; never row-based exceptions."""
    a,b=before.signature(),after.signature();allowed=allowed or {}
    changes=[]
    for key in a:
        if key=='protected_tasks':
            for uid in set(a[key])|set(b[key]):
                for field in set(a[key].get(uid,{}))|set(b[key].get(uid,{})):
                    if a[key].get(uid,{}).get(field)!=b[key].get(uid,{}).get(field) and field not in allowed.get(uid,[]):
                        changes.append(f'task {uid}: unauthorized {field} change')
        elif a[key]!=b[key]:changes.append(f'unauthorized {key} change')
    return changes

def deltas(before,after):
    key=lambda f:(f['code'],tuple(f['tasks']),f['severity'],f.get('identity',f['code']))
    a={key(f):f for f in before};b={key(f):f for f in after}
    return {'new':[b[k] for k in b.keys()-a.keys()], 'existing':[b[k] for k in b.keys()&a.keys()],
            'resolved':[a[k] for k in a.keys()-b.keys()],
            'changed':[{'before':a[k],'after':b[k]} for k in a.keys()&b.keys() if a[k]['message']!=b[k]['message']]}

def verdict(findings, verified=False, applied=True):
    if not applied or any(f['severity']=='ERROR' for f in findings):return 'FAIL'
    if not verified or any(f['severity']=='UNVERIFIED' for f in findings):return 'UNVERIFIED'
    return 'PASS'

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('xml');p.add_argument('--policy',required=True)
    p.add_argument('--evidence');p.add_argument('--output',required=True);args=p.parse_args()
    policy=json.loads(Path(args.policy).read_text(encoding='utf-8-sig'))
    evidence=json.loads(Path(args.evidence).read_text()) if args.evidence else {}
    findings=audit(Schedule(args.xml),policy,evidence)
    result={'status':verdict(findings,False),'findings':findings,'note':'Standalone audit cannot prove saved-file verification'}
    Path(args.output).write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(result['status'])
if __name__=='__main__':main()
