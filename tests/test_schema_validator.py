import csvw
from poseidon.utils import PoseidonSchemaError
from poseidon.schema_validator import ColumnValidator, TableValidator
import pytest

class TestColumnSchema:

    def test_match_requires_columnName(self):
        column_def = csvw.Column(datatype="string")
        with pytest.raises(PoseidonSchemaError) as e:
            v = ColumnValidator(column_def)
        assert str(e.value) == f"Column {column_def} needs a name"

    def test_match(self):
        
        column_def = csvw.Column(name="MyName", datatype="string")

        v = ColumnValidator(column_def)
        assert v.match(column_def)
        
        column_def2 = csvw.Column(name="MyName2", datatype="string")
        assert not v.match(column_def2)

        # matching is only by name, not datatype
        column_def2 = csvw.Column(name="MyName", datatype="integer")
        assert v.match(column_def2)
    
    def test_validate(self):
        column_def = csvw.Column(name="MyName", datatype="string")
        v = ColumnValidator(column_def)

        # should pass with itself
        v.validate(column_def)

        # should raise with a wrong name
        column_def2 = csvw.Column(name="MyName2", datatype="string")
        with pytest.raises(PoseidonSchemaError) as e:
            v.validate(column_def2)  
        assert str(e.value) == "expected column name \"MyName\" but got \"MyName2\""

        # should raise with a wrong type
        column_def2 = csvw.Column(name="MyName", datatype="integer")
        with pytest.raises(PoseidonSchemaError) as e:
            v.validate(column_def2)  
        assert str(e.value) == "For column \"MyName\" expected column type \"string\" but got \"integer\""
        
        # should raise with a wrong complex type
        column_def2 = csvw.Column(name="MyName", datatype={"base" : "string", "format" : "[Tooth|Petrous|OtherBone|OtherTissue]"})
        with pytest.raises(PoseidonSchemaError) as e:
            v.validate(column_def2)  
        assert str(e.value) == ("For column \"MyName\" expected column type "
            "\"string\" but got \"OrderedDict([('base', 'string'), "
            "('format', '[Tooth|Petrous|OtherBone|OtherTissue]')])\"")

class TestTableSchema:
    def test_constructor_needs_primary_key(self):
        t = csvw.Table.fromvalue({
            "@context": ["http://www.w3.org/ns/csvw", {"@language": "en"}],
            "tableSchema": {
                "columns": [
                    {"name": "ID", "datatype": {"base": "string", "minLength": 3}},
                    {"name" : "test", "datatype": "string"}
                ]
            }
        })
        with pytest.raises(PoseidonSchemaError) as e:
            v = TableValidator(t)
        assert str(e.value) == "TableValidator: Error for table with columns [ID, test]: Poseidon tables require exactly one primary key defined."

    def test_tables_need_primary_key(self):
        t = csvw.Table.fromvalue({
            "@context": ["http://www.w3.org/ns/csvw", {"@language": "en"}],
            "tableSchema": {
                "columns": [
                    {"name": "ID", "datatype": {"base": "string", "minLength": 3}},
                    {"datatype": "string"}
                ],
                "primaryKey" : "PKey",
            }
        })
        v = TableValidator(t)
        t2 = csvw.Table.fromvalue({
            "@context": ["http://www.w3.org/ns/csvw", {"@language": "en"}],
            "tableSchema": {
                "columns": [
                    {"name": "ID", "datatype": {"base": "string", "minLength": 3}},
                    {"name": "test", "datatype": "string"}
                ]
            }
        })
        with pytest.raises(PoseidonSchemaError) as e:
            v.match(t2)
        assert str(e.value) == "TableValidator: Error for table with columns [ID, test]: Poseidon tables require exactly one primary key defined."

    def test_tables_match_primary_key(self):
        t = csvw.Table.fromvalue({
            "@context": ["http://www.w3.org/ns/csvw", {"@language": "en"}],
            "tableSchema": {
                "columns": [
                    {"name": "ID", "datatype": {"base": "string", "minLength": 3}},
                    {"name": "Test", "datatype": "string"}
                ],
                "primaryKey" : "PKey",
            }
        })
        v = TableValidator(t)
        t2 = csvw.Table.fromvalue({
            "@context": ["http://www.w3.org/ns/csvw", {"@language": "en"}],
            "tableSchema": {
                "columns": [
                    {"name": "ID", "datatype": {"base": "string", "minLength": 3}},
                    {"datatype": "string"}
                ],
                "primaryKey" : "PKey2",
            }
        })
        assert not v.match(t2)
