import csvw
import schema_validator
import attr

@attr.s
class PoseidonModule:
    table_group : csvw.TableGroup = attr.ib()

    def __attrs_post_init__(self):
        self._validate_tables()
        self._validate_foreign_keys()
        self._validate_metadata()
        self._validate_genotype_data()
    
    def _validate_tables(self):
        pass

    def _validate_foreign_keys():
        pass

    def _validate_metadata():
        pass

    def _validate_genotype_data():
        pass

