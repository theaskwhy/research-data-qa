# Structural validator schema format

The validator accepts a JSON object with a `tables` object. Each table maps a CSV filename stem to `required_columns`, an optional `id_column`, and optional `foreign_keys`.

```json
{
  "tables": {
    "records": {
      "required_columns": ["record_id", "name", "source_id"],
      "id_column": "record_id",
      "foreign_keys": [{"column": "source_id", "table": "sources", "target_column": "source_id"}]
    },
    "sources": {
      "required_columns": ["source_id", "url"],
      "id_column": "source_id"
    }
  }
}
```

For each table, the validator reads `<table>.csv` from the input directory. Required columns and ID uniqueness are checked when configured. Foreign keys are checked against the configured target column. A missing table, required column, empty/duplicate ID, or unresolved nonempty foreign key is a high-severity structural finding. Empty optional foreign keys are ignored. This format does not express domain truth, external-source verification, privacy, licensing, or whether the schema itself is appropriate.
