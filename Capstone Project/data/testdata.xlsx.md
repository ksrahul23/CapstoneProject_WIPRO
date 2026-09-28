# Optional Excel test data

If you'd rather drive the suite from Excel instead of JSON, add a file at
`data/testdata.xlsx` with a single sheet named `TestData` and these
columns in row 1:

| first_name | last_name | email_template | telephone | password | search_term | quantity_to_add | updated_quantity |
|---|---|---|---|---|---|---|---|

`utils/data_reader.py` checks for this file first and falls back to
`testdata.json` automatically if it isn't present, so no code changes
are needed to switch between the two.
