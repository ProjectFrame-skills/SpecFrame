import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'integrations/agensi'))
import transport


class TransportBoundary(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.session='session-a';self.owner='owner-a'
        binding=self.root/'.specframe/agensi/session-a.json';binding.parent.mkdir(parents=True)
        self.state=self.root/'.specframe/owner-a.json'
        self.state.write_text(json.dumps({'format':1,'owner':self.owner,'sections':{'GOAL':'goal','SCOPE':'scope','CONSTRAINTS':'draft','R':'confirmed exception','OPEN':'reverse transition unresolved'},'focus':['R'],'pending':['OPEN'],'next':'ask','approval':'draft'}))
        binding.write_text(json.dumps({'format':1,'session':self.session,'owner':self.owner,'state':'.specframe/owner-a.json','slug':'specframe','server':'agensi_live'}))
        source=(ROOT/'skills/specframe/scripts/state.py').read_text()
        self.event={'hook_event_name':'PostToolUse','cwd':str(self.root),'session_id':self.session,'tool_name':'mcp__agensi_live__get_skill','tool_input':{'slug':'specframe','file':'scripts/state.py'},'tool_response':{'content':[{'type':'text','text':transport.HEADER+source}]}}

    def test_exact_delivery_execution_and_cleanup(self):
        before=self.state.read_bytes();self.assertIsNotNone(transport.prepare(self.event))
        self.assertEqual(transport.run(self.root,self.session,['read','R']),0)
        self.assertEqual(before,self.state.read_bytes())
        self.assertFalse(list(self.root.glob('.specframe-exec-*')))
        self.assertFalse(list((self.root/'.specframe/agensi').glob('.prepared-*')))

    def test_wrong_partial_error_delivery_is_not_staged(self):
        for event in [dict(self.event,tool_name='mcp__other__get_skill'),dict(self.event,tool_input={'slug':'other','file':'scripts/state.py'}),dict(self.event,tool_response={'isError':True}),dict(self.event,tool_response={'content':[{'type':'text','text':transport.HEADER+'print(1)'}]})]:
            self.assertIsNone(transport.prepare(event));self.assertFalse(list(self.root.glob('.specframe-exec-*')))

    def test_tamper_and_owner_override_refused_and_cleaned(self):
        transport.prepare(self.event);selection=transport.select(self.root,self.session);path=transport.prepared(selection,self.session);path.write_text('raise Exception("bad")')
        with self.assertRaisesRegex(ValueError,'changed'):transport.run(self.root,self.session,['resume'])
        self.assertFalse(path.exists())
        transport.prepare(self.event)
        with self.assertRaisesRegex(ValueError,'bound'):transport.run(self.root,self.session,['--state=/tmp/other','save'])
        self.assertFalse(list(self.root.glob('.specframe-exec-*')))

    def test_new_failed_delivery_invalidates_unused_preparation(self):
        transport.prepare(self.event)
        self.assertIsNone(transport.prepare(dict(self.event,tool_response={'isError':True})))
        self.assertFalse(list(self.root.glob('.specframe-exec-*')))

    def test_lifecycle_cleanup_and_unrelated_session(self):
        self.assertIsNone(transport.prepare(dict(self.event,session_id='another')))
        transport.prepare(self.event);transport.cleanup(self.root,self.session)
        self.assertFalse(list(self.root.glob('.specframe-exec-*')))
        self.assertEqual(json.loads(self.state.read_text())['pending'],['OPEN'])

if __name__=='__main__':unittest.main()
