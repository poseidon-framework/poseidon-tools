import csvw

tg = csvw.TableGroup.from_file('tests/testModules/myTestModule1/metadata.json')

t = tg.tabledict['sites.csv']

print(t.tableSchema.primaryKey)
