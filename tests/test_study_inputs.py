import json
import unittest
from pathlib import Path


class StudyInputTests(unittest.TestCase):
    def test_domain_references_and_units(self):
        data=json.loads((Path(__file__).resolve().parents[1]/'fixtures/study-input.json').read_text())
        from chainledger.service import SupplyChain
        with SupplyChain() as app:
            for source in sorted({r['source'] for r in data['envelopes']}):
                app.consumer.register(source)
            for envelope in data['envelopes']:
                result=app.consumer.submit(envelope)
                self.assertEqual(result['state'],'applied')
            self.assertEqual(str(app.graph.stock('part-a')),'4')
            self.assertEqual(str(app.graph.stock('part-b')),'3')
