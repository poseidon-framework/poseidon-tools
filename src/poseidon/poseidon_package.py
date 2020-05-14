import csvw

def identify_table(tablegroup, table):
    if table not in ["Sites", "Individuals", "C14dating", "Sequencing", "Genotyping"]:
        raise Poseidon

class PoseidonModule:
    def __init__(self, csvw_tablegroup):
        self.csvw_tablegroup = csvw_tablegroup
        self.sites_table_name = identify_sites_table(self.csvw_tablegroup)
        self.validate()
        tg.check_referential_integrity()

    
    @classmethod
    def fromMetadataFile(self, metadatafile):
        tg = csvw.TableGroup.from_file(metadatafile)
        return PoseidonModule(tg)

    def validate(self):

