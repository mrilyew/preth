from executables.representations.WebServices_Vk.Post import Post

class Message(Post):
    vk_type = "message"

    class Extractor(Post.Extractor):
        async def __response(self, i = {}):
            items_ids = i.get('ids')

            response = await self.vkapi.call("messages.getById", {"message_ids": (",".join(items_ids)), "extended": 1})

            return response
