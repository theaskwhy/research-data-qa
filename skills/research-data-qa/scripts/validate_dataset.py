#!/usr/bin/env python3
"""Read-only, schema-driven structural checks for a directory of CSV tables."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def audit(folder: Path, schema: dict) -> dict:
    findings = []
    tables = schema.get('tables')
    if not isinstance(tables, dict) or not tables:
        raise ValueError('Schema must contain a non-empty tables object')
    loaded = {}
    counts = {}

    def flag(table, check, detail, severity='HIGH'):
        findings.append({'severity': severity, 'table': table, 'check': check, 'detail': detail})

    for name, spec in tables.items():
        if not isinstance(name, str) or not name or '/' in name or name.endswith('.csv'):
            raise ValueError('Table keys must be simple CSV filename stems')
        if not isinstance(spec, dict):
            raise ValueError(f'Table schema for {name} must be an object')
        path = folder / f'{name}.csv'
        if not path.is_file():
            flag(name, 'MISSING_TABLE', f'{path.name} was not supplied')
            loaded[name] = []
            counts[name] = 0
            continue
        with path.open('r', encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            required = spec.get('required_columns', [])
            if not isinstance(required, list) or not all(isinstance(c, str) for c in required):
                raise ValueError(f'required_columns for {name} must be a list of strings')
            for column in required:
                if column not in headers:
                    flag(name, 'MISSING_COLUMN', column)
            if not headers:
                flag(name, 'MISSING_HEADER', 'CSV has no header row')
                rows = []
            else:
                rows = [row for row in reader if any((value or '').strip() for value in row.values())]
        loaded[name] = rows
        counts[name] = len(rows)
        id_column = spec.get('id_column')
        if id_column:
            if id_column not in headers:
                flag(name, 'MISSING_ID_COLUMN', id_column)
            else:
                values = [(row.get(id_column) or '').strip() for row in rows]
                for value, count in Counter(values).items():
                    if not value:
                        flag(name, 'EMPTY_ID', id_column)
                    elif count > 1:
                        flag(name, 'DUPLICATE_ID', f'{id_column}={value} occurs {count} times')

    for name, spec in tables.items():
        for relation in spec.get('foreign_keys', []):
            if not isinstance(relation, dict):
                raise ValueError(f'foreign_keys entries for {name} must be objects')
            column = relation.get('column')
            target_table = relation.get('table')
            target_column = relation.get('target_column')
            if not all(isinstance(x, str) and x for x in (column, target_table, target_column)):
                raise ValueError(f'Invalid foreign key definition for {name}')
            if target_table not in tables:
                raise ValueError(f'Foreign key target table {target_table} is not defined')
            if not any(row.get(column) not in (None, '') for row in loaded[name]):
                continue
            target_ids = {(row.get(target_column) or '').strip() for row in loaded[target_table]}
            if target_column not in tables[target_table].get('required_columns', []) and tables[target_table].get('id_column') != target_column:
                flag(name, 'UNDECLARED_TARGET_COLUMN', f'{target_table}.{target_column}', 'MEDIUM')
            for row in loaded[name]:
                value = (row.get(column) or '').strip()
                if value and value not in target_ids:
                    flag(name, 'BROKEN_REFERENCE', f'{column}={value} has no {target_table}.{target_column}')

    held = any(item['severity'] == 'HIGH' for item in findings)
    return {
        'audit_type': 'OFFLINE_STRUCTURAL_ONLY',
        'row_counts': counts,
        'structural_gate': 'HOLD' if held else 'PASS',
        'external_source_verification': 'NOT_RUN',
        'rights_and_privacy_review': 'NOT_RUN',
        'downstream_use_gate': 'HOLD',
        'findings': findings,
        'disclaimer': 'Structural checks do not establish source truth, freshness, rights, or suitability for downstream use.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path, help='Directory of CSV tables')
    parser.add_argument('--schema', required=True, type=Path, help='JSON schema contract')
    parser.add_argument('--output', type=Path, help='Optional JSON report path')
    args = parser.parse_args()
    if not args.input.is_dir():
        parser.error('Input must be an existing directory')
    try:
        schema = json.loads(args.schema.read_text(encoding='utf-8'))
        result = audit(args.input, schema)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + '\n', encoding='utf-8')
    print(output)
    return 2 if result['structural_gate'] == 'HOLD' else 0


if __name__ == '__main__':
    raise SystemExit(main())
