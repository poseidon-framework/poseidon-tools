import csvw

tg = csvw.TableGroup.from_file('tests/testModules/myTestModule1/metadata.json')

t = csvw.Table.fromvalue({
    "@context": ["http://www.w3.org/ns/csvw", {"@language": "en"}],
    "tables": [
        "tableSchema": {
            "columns": [
                {"name": "ID", "datatype": {"base": "string", "minLength": 3}},
                {"name": "ID", "datatype": {"base": "string", "minLength": 3}},
                {"name" : "test", "datatype": "string"}
            ],
            "primaryKey" : "ID"
        }
    ]
})

print(t.tableSchema.primaryKey)
