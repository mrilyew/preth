from executables.representations.WebServices_Vk import BaseVkItemId
from submodules.Web.DownloadManager import download_manager
from declarable.ArgumentsTypes import BooleanArgument
from utils.MainUtils import valid_name
from db.DbInsert import db_insert
from app.App import logger
from pathlib import Path
import os

class Doc(BaseVkItemId):
    @classmethod
    def declare(cls):
        params = {}
        params["download"] = BooleanArgument({
            "default": True
        })

        return params

    class Extractor(BaseVkItemId.Extractor):
        async def __response(self, i = {}):
            items_ids = i.get('ids')

            response = await self.vkapi.call("docs.getById", {"docs": (",".join(items_ids)), "extended": 1})

            return response

        async def item(self, item, link_entities):
            self.outer._insertVkLink(item, self.args.get('vk_path'))

            item_id = f"{item.get('owner_id')}_{item.get('id')}"
            private_url = item.get("private_url")
            is_do_unlisted = self.args.get("unlisted") == 1

            logger.log(message=f"Recieved document {item_id}",section="Vk!Doc",kind=logger.KIND_MESSAGE)

            main_su = None
            item_ext = item.get("ext")
            item_title = item.get("title")
            file_name = valid_name(item_title + "." + item_ext)
            item_url = item.get("url")
            item_filesize = item.get("size", 0)

            if self.args.get("download") == True:
                main_su = db_insert.storageUnit()
                temp_dir = main_su.temp_dir
                save_path = Path(os.path.join(temp_dir, file_name))

                await download_manager.addDownload(end=item_url,dir=save_path)

                main_su.set_main_file(save_path)

                logger.log(message=f"Download file for doc {item_id}",section="Vk!Doc",kind=logger.KIND_SUCCESS)

            cu = db_insert.contentFromJson({
                "links": [main_su],
                "link_main": 0,
                "name": item_title,
                "source": {
                    'type': 'vk',
                    'vk_type': 'doc',
                    'content': item_id
                },
                "content": item,
                "unlisted": is_do_unlisted,
                "declared_created_at": item.get("date"),
            })

            link_entities.append(cu)
