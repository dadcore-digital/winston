from discord.ext.menus import MenuPages
from discord import Embed

class PermissiveMenuPages(MenuPages):

    def __init__(self, source, **kwargs):
        self._source = source
        self.current_page = 0
        super().__init__(source, timeout=None, **kwargs)

    @property
    def source(self):
        """:class:`PageSource`: The source where the data comes from."""
        return self._source


    def reaction_check(self, payload):
        """
        Overriding this so anyone can interact with a paginator, not just author.
        """

        if payload.message_id != self.message.id:
            return False
        
        # Removing this check, except don't let the bot trigger itself.
        if payload.user_id == self.bot.user.id:
            return False

        return payload.emoji in self.buttons
