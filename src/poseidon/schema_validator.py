import attr
from poseidon.utils import PoseidonSchemaError
from csvw import Datatype, Column, Table
from typing import Dict

@attr.s
class ColumnValidator:
    '''A class to validate a given csvw column definition'''

    column_def : Column = attr.ib()

    def __attrs_post_init__(self):
        if self.column_def.name is None:
            raise PoseidonSchemaError(f"Column {self.column_def} needs a name")

    def match(self, column_def : Column) -> bool:
        '''check whether the name of a column matches the name of the column passed to the constructor'''
        return self.column_def.name == column_def.name
    
    def validate(self, column_def : Column) -> None:
        '''raises an error if the column definition doesn't match in name and type'''
        if not self.match(column_def):
            raise PoseidonSchemaError(
                f"expected column name \"{self.column_def.name}\" but got \"{column_def.name}\"")
        if self.column_def.datatype != column_def.datatype:
            raise PoseidonSchemaError(f"For column \"{column_def.name}\" expected column "
                f"type \"{self.column_def.datatype.asdict()}\" but got \"{column_def.datatype.asdict()}\"")



@attr.s
class TableValidator:
    '''A class to validate an entire table'''

    csvw_table_def : Table = attr.ib()

    @staticmethod    
    def check_has_primary_key(csvw_table_def):
        p = csvw_table_def.tableSchema.primaryKey 
        if p is None or len(p) != 1:
            print([c.name for c in csvw_table_def.tableSchema.columns])
            cols = ", ".join([c.name for c in csvw_table_def.tableSchema.columns])
            raise PoseidonSchemaError(f"TableValidator: Error for table with columns [{cols}]: "
                "Poseidon tables require exactly one primary key defined.")

    def __attrs_post_init__(self):
        self.check_has_primary_key(self.csvw_table_def)


    def match(self, csvw_table_def : Table) -> bool:
        self.check_has_primary_key(csvw_table_def)

