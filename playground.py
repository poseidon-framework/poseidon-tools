import csvw
from csvw.db import Database

tg = csvw.TableGroup.from_file('tests/testModules/myTestModule1/metadata_inkl_schemas.json')

tg.check_referential_integrity()

db = Database(tg, fname='test.sqlite')
db.write_from_tg()

# for row in tg.tables[1].iterdicts():
#     print("Row:")
#     for k, v in row.items():
#         print(f"  {k}: {v}")

# tg.check_referential_integrity()
