"""Offline adversarial tests. No desktop application is opened."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
from guardian import Schedule,audit,compare_protected,deltas,verdict,NS

def fixture(path, links=None, extra=None):
    root=ET.Element('Project',xmlns=NS['p']);tasks=ET.SubElement(root,'Tasks')
    for uid,name in [('10','Mobilize'),('20','Install'),('30','Completion')]:
        t=ET.SubElement(tasks,'Task')
        values={'UID':uid,'GUID':'fixture-'+uid,'Name':name,'Start':'2026-11-02T08:00:00',
                'Finish':'2026-11-02T17:00:00','Duration':'PT8H0M0S','Manual':'0','ConstraintType':'0'}
        values.update((extra or {}).get(uid,{}))
        for k,v in values.items():ET.SubElement(t,k).text=v
        for a,b,kind,lag in (links if links is not None else [('10','20','1','0'),('20','30','1','0')]):
            if b==uid:
                link=ET.SubElement(t,'PredecessorLink')
                for k,v in {'PredecessorUID':a,'Type':kind,'LinkLag':lag,'LagFormat':'7'}.items():ET.SubElement(link,k).text=v
    ET.ElementTree(root).write(path,encoding='utf-8',xml_declaration=True)
    return Schedule(path)

POLICY={'completion_uid':'30','open_end_exceptions':{'10':{'predecessor':'Authorized project start'},'30':{'successor':'Intended completion milestone'}}}

class AuditTests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'fixture.xml'
    def tearDown(self):self.tmp.cleanup()
    def codes(self,s):return {f['code'] for f in audit(s,POLICY)}
    def test_cycles_missing_disconnected_self_duplicate(self):
        s=fixture(self.path,[('10','20','1','0'),('20','10','1','0'),('99','20','1','0'),('20','20','1','0'),('10','20','1','0')])
        self.assertTrue({'CYCLE','MISSING_TASK','DISCONNECTED','SELF_LINK','DUPLICATE_LINK'}<=self.codes(s))
    def test_no_native_evidence_never_passes(self):
        s=fixture(self.path);f=audit(s,POLICY)
        self.assertEqual(verdict(f,False),'UNVERIFIED')
    def test_actual_conflict_history_is_unchanged(self):
        s=fixture(self.path,extra={'20':{'ActualStart':'2026-11-02T08:00:00'}});original=self.path.read_bytes()
        evidence={'native_recalculated':True,'edges':{'|'.join(l):{'verified':True,'minimum':'2026-11-03T08:00:00'} for l in s.links}}
        self.assertIn('OUT_OF_SEQUENCE_ACTUAL',{x['code'] for x in audit(s,POLICY,evidence)})
        self.assertEqual(original,self.path.read_bytes())
    def test_manual_hard_constraint_and_deadline(self):
        s=fixture(self.path,extra={'20':{'Manual':'1','ConstraintType':'3','TotalSlack':'-480','Deadline':'2026-11-01T17:00:00'}})
        self.assertTrue({'MANUAL','HARD_CONSTRAINT','NEGATIVE_FLOAT','MISSED_DEADLINE'}<=self.codes(s))
    def test_stable_uid_not_row_order(self):
        a=fixture(self.path);other=Path(self.tmp.name)/'reordered.xml'
        root=ET.parse(self.path);ts=root.find('p:Tasks',NS);ts[:]=list(reversed(list(ts)));root.write(other)
        self.assertEqual(compare_protected(a,Schedule(other)),[])
    def test_existing_new_resolved(self):
        a=audit(fixture(self.path),POLICY)
        b=audit(fixture(self.path,extra={'20':{'Manual':'1'}}),POLICY)
        d=deltas(a,b);self.assertIn('MANUAL',{x['code'] for x in d['new']});self.assertTrue(d['existing']);self.assertEqual(d['resolved'],[])
    def test_unauthorized_duration_and_actual_rewrite(self):
        a=fixture(self.path);b=fixture(Path(self.tmp.name)/'b.xml',extra={'20':{'Duration':'PT1H0M0S','ActualStart':'2026-11-01T08:00:00'}})
        self.assertEqual(len(compare_protected(a,b)),2)
        self.assertEqual(len(compare_protected(a,b,{'20':['Duration']})),1)
    def test_all_four_types_and_lag_preserved(self):
        a=fixture(self.path,[('10','20',k,'4800') for k in ('0','1','2','3')]);b=fixture(Path(self.tmp.name)/'b.xml',[('10','20',k,'0') for k in ('0','1','2','3')])
        self.assertIn('unauthorized links change',compare_protected(a,b))
    def test_construction_rules_and_warnings(self):
        s=fixture(self.path,[('10','20','1','-50000'),('20','30','1','0')]);policy=copy.deepcopy(POLICY)
        policy['required_sequences']=[{'before':'20','after':'10','reason':'Inspection before concealment required by specification'}]
        self.assertTrue({'LEAD','LONG_LAG','CONSTRUCTION_SEQUENCE'}<={f['code'] for f in audit(s,policy)})
    def test_blocked_request_is_fail_even_without_findings(self):self.assertEqual(verdict([],True,False),'FAIL')
    def test_ss_reachability_does_not_certify_inspection_sequence(self):
        s=fixture(self.path,[('10','20','3','0'),('20','30','1','0')])
        policy=copy.deepcopy(POLICY)
        policy['required_sequences']=[{'before':'10','after':'20','reason':'Inspection completed before concealment'}]
        evidence={'native_recalculated':True,'edges':{'|'.join(l):{'verified':True,'minimum':'2026-11-02T08:00:00'} for l in s.links}}
        f=audit(s,policy,evidence)
        self.assertIn('CONSTRUCTION_REQUIREMENT_UNVERIFIED',{x['code'] for x in f})
        self.assertEqual(verdict(f,True),'UNVERIFIED')
    def test_changed_violation_remains_existing(self):
        s=fixture(self.path)
        evidence={'native_recalculated':True,'edges':{'|'.join(l):{'verified':True,'minimum':'2026-11-03T08:00:00'} for l in s.links}}
        a=audit(s,POLICY,evidence)
        for bound in evidence['edges'].values():bound['minimum']='2026-11-04T08:00:00'
        b=audit(s,POLICY,evidence);d=deltas(a,b)
        self.assertEqual(d['new'],[]);self.assertEqual(d['resolved'],[])
        self.assertEqual(len(d['changed']),2)

if __name__=='__main__':unittest.main(verbosity=2)
