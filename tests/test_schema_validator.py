import csvw
from poseidon.utils import PoseidonSchemaError
from poseidon.schema_validator import ColumnValidator, TableValidator
import pytest

class TestColumnSchema:

    def test_init_without_name(self):
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
        
        # should raise with wrong required field
        column_def2 = csvw.Column(name="MyName", datatype="string", required=True)
        with pytest.raises(PoseidonSchemaError) as e:
            v.validate(column_def2)  
        assert str(e.value) == ("For column \"MyName\": expected column to be not required, but got required")
        
        column_def = csvw.Column(name="MyName", datatype="string", required=True)
        v = ColumnValidator(column_def)

        column_def2 = csvw.Column(name="MyName", datatype="string")
        with pytest.raises(PoseidonSchemaError) as e:
            v.validate(column_def2)  
        assert str(e.value) == ("For column \"MyName\": expected column to be required, but got not required")


class TestTableSchema:
    
    def test_init_needs_term(self):
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
        assert str(e.value) == "TableValidator: Needs RDF term"
    
    def test_tables_match_rdf_term(self):
        t = csvw.Table.fromvalue({
            "@context": ["http://www.w3.org/ns/csvw", {"@language": "en"}],
            "dc:conformsTo" : "http://w3id.org/poseidon/myterm",
            "tableSchema": {
                "columns": [
                    {"name": "ID", "datatype": {"base": "string", "minLength": 3}, "required": True},
                    {"name": "Test", "datatype": "string"}
                ],
                "primaryKey" : "ID",
            }
        })
        v = TableValidator(t)
        t2 = csvw.Table.fromvalue({
            "@context": ["http://www.w3.org/ns/csvw", {"@language": "en"}],
            "tableSchema": {
                "columns": [
                    {"name": "ID2", "datatype": {"base": "string", "minLength": 3}, "required": True},
                    {"datatype": "string"}
                ],
                "primaryKey" : "ID2",
            }
        })
        assert not v.match(t2)

    def test_table_validate_same_table(self):
        t = csvw.Table.fromvalue({
            "@context": ["http://www.w3.org/ns/csvw", {"@language": "en"}],
            "tableSchema": {
                "columns": [
                    {"name": "ID", "datatype": {"base": "string", "minLength": 3}, "required": True},
                    {"name": "Test", "datatype": "string"}
                ],
                "primaryKey" : "ID",
            }
        })
        v = TableValidator("Sites", t)
        v.validate(t)
    
    def test_table_validate_fail_missing_cols(self):
        t = csvw.Table.fromvalue({
            "@context": ["http://www.w3.org/ns/csvw", {"@language": "en"}],
            "tableSchema": {
                "columns": [
                    {"name": "ID", "datatype": {"base": "string", "minLength": 3}, "required": True},
                    {"name": "Test", "datatype": "string", "required" : True}
                ],
                "primaryKey" : "ID",
            }
        })
        v = TableValidator("Sites", t)
        t2 = csvw.Table.fromvalue({
            "@context": ["http://www.w3.org/ns/csvw", {"@language": "en"}],
            "tableSchema": {
                "columns": [
                    {"name": "ID", "datatype": {"base": "string", "minLength": 3}, "required" : True}
                ],
                "primaryKey" : "ID",
            }
        })
        with pytest.raises(PoseidonSchemaError) as e:
            v.validate(t2)
        assert str(e.value) == "TableValidator: Table \"Sites\" misses required column \"Test\""

    def test_table_validate_succeed_non_required_missing_cols(self):
        t = csvw.Table.fromvalue({
            "@context": ["http://www.w3.org/ns/csvw", {"@language": "en"}],
            "tableSchema": {
                "columns": [
                    {"name": "ID", "datatype": {"base": "string", "minLength": 3}, "required": True},
                    {"name": "Test", "datatype": "string"}
                ],
                "primaryKey" : "ID",
            }
        })
        v = TableValidator("Sites", t)
        t2 = csvw.Table.fromvalue({
            "@context": ["http://www.w3.org/ns/csvw", {"@language": "en"}],
            "tableSchema": {
                "columns": [
                    {"name": "ID", "datatype": {"base": "string", "minLength": 3}, "required": True}
                ],
                "primaryKey" : "ID",
            }
        })
        v.validate(t2)

    def test_table_validate_fail_wrong_column_props(self):
        t = csvw.Table.fromvalue({
            "@context": ["http://www.w3.org/ns/csvw", {"@language": "en"}],
            "tableSchema": {
                "columns": [
                    {"name": "ID", "datatype": {"base": "string", "minLength": 3}, "required": True},
                    {"name": "Test", "datatype": "string"}
                ],
                "primaryKey" : "ID",
            }
        })
        v = TableValidator("Sites", t)
        t2 = csvw.Table.fromvalue({
            "@context": ["http://www.w3.org/ns/csvw", {"@language": "en"}],
            "tableSchema": {
                "columns": [
                    {"name": "ID", "datatype": {"base": "string", "minLength": 3}, "required": True},
                    {"name": "Test", "datatype": "integer"}
                ],
                "primaryKey" : "ID",
            }
        })

        with pytest.raises(PoseidonSchemaError) as e:
            v.validate(t2)
        assert str(e.value) == "TableValidator: Table \"Sites\": For column \"Test\" expected column type \"string\" but got \"integer\""

        