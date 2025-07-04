from executables.acts import BaseAct
from declarable.ArgumentsTypes import CsvArgument
from db.Models.Content.ContentUnit import ContentUnit

class GetById(BaseAct):
    category = 'ContentUnits'

    @classmethod
    def declare(cls):
        params = {}
        params["ids"] = CsvArgument({
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def execute(self, i = {}):
        ids = i.get('ids')

        items = ContentUnit.ids(ids)
        fnl = []
        
        for item in items:
            fnl.append(item.api_structure())

        return fnl
