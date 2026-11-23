import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name('validate_dataset.py')


def write_csv(path, headers, rows):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


class DatasetValidatorTests(unittest.TestCase):
    def run_validator(self, bad=False):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            data = root / 'data'
            data.mkdir()
            write_csv(data / 'records.csv', ['record_id', 'source_id'], [
                {'record_id': 'R1', 'source_id': 'MISSING' if bad else 'S1'},
                {'record_id': 'R1' if bad else 'R2', 'source_id': 'S1'},
            ])
            write_csv(data / 'sources.csv', ['source_id', 'url'], [{'source_id': 'S1', 'url': 'https://example.test'}])
            schema = root / 'schema.json'
            schema.write_text(json.dumps({'tables': {
                'records': {'required_columns': ['record_id', 'source_id'], 'id_column': 'record_id',
                            'foreign_keys': [{'column': 'source_id', 'table': 'sources', 'target_column': 'source_id'}]},
                'sources': {'required_columns': ['source_id', 'url'], 'id_column': 'source_id'}
            }}), encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPT), '--input', str(data), '--schema', str(schema)], capture_output=True, text=True)
            return result.returncode, json.loads(result.stdout)

    def test_valid_structure_does_not_approve_downstream_use(self):
        code, report = self.run_validator()
        self.assertEqual(code, 0)
        self.assertEqual(report['structural_gate'], 'PASS')
        self.assertEqual(report['external_source_verification'], 'NOT_RUN')
        self.assertEqual(report['downstream_use_gate'], 'HOLD')

    def test_duplicate_id_and_broken_reference_hold(self):
        code, report = self.run_validator(bad=True)
        self.assertEqual(code, 2)
        checks = {finding['check'] for finding in report['findings']}
        self.assertTrue({'DUPLICATE_ID', 'BROKEN_REFERENCE'} <= checks)


if __name__ == '__main__':
    unittest.main()
