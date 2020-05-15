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
        if not self.column_def.required and column_def.required:
            raise PoseidonSchemaError(f"For column \"{column_def.name}\": expected column to be not required, but got required")
        if self.column_def.required and not column_def.required:
            raise PoseidonSchemaError(f"For column \"{column_def.name}\": expected column to be required, but got not required")



@attr.s
class TableValidator:
    '''A class to validate an entire table'''

    table_name : str = attr.ib()
    csvw_table_def : Table = attr.ib()

    @staticmethod
    def _check_has_primary_key(table_name, csvw_table_def):
        p = csvw_table_def.tableSchema.primaryKey 
        if p is None or len(p) != 1:
            print([c.name for c in csvw_table_def.tableSchema.columns])
            cols = ", ".join([c.name for c in csvw_table_def.tableSchema.columns])
            raise PoseidonSchemaError(f"TableValidator: Error for table \"{table_name}\" with columns [{cols}]: "
                "Poseidon tables require exactly one primary key defined.")
    
    @staticmethod
    def _check_primary_key_col_exists(table_name, csvw_table_def):
        pkey = csvw_table_def.tableSchema.primaryKey[0]
        pkey_cols = [c for c in csvw_table_def.tableSchema.columns if c.name == pkey]
        cols = ", ".join([c.name for c in csvw_table_def.tableSchema.columns])
        if len(pkey_cols) != 1:
            raise PoseidonSchemaError(f"TableValidator: Error for table \"{table_name}\" with columns [{cols}]: "
                f"Table needs exactly one column with the name of the primary key \"{pkey}\"")
        else:
            if not pkey_cols[0].required:
                raise PoseidonSchemaError(f"TableValidator: Error for table \"{table_name}\" with columns [{cols}]: "
                    f"Primary key column \"{pkey}\" must be required")

    def __attrs_post_init__(self):
        self._check_has_primary_key(self.table_name, self.csvw_table_def)
        self._check_primary_key_col_exists(self.table_name, self.csvw_table_def)

    def match(self, csvw_table_def : Table) -> bool:
        self._check_has_primary_key(self.table_name, csvw_table_def)

    def validate(self, csvw_table_def : Table) -> None:
        for col in self.csvw_table_def.tableSchema.columns:
            v = ColumnValidator(col)
            for col2 in csvw_table_def.tableSchema.columns:
                if v.match(col2):
                    try:
                        v.validate(col2)
                        break
                    except PoseidonSchemaError as e:
                        raise PoseidonSchemaError(f"TableValidator: Table \"{self.table_name}\": " + str(e))
            else:
                if col.required:
                    raise PoseidonSchemaError(f"TableValidator: Table \"{self.table_name}\" misses required column \"{col.name}\"")