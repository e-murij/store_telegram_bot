from handlers.handler_commands import HandlerCommands
from handlers.handler_inline_query import HandlerInlineQuery
from handlers.handler_text_commands import HandlerAllTextCommands


class HandlerMain:
    def __init__(self, bot):
        self.bot = bot
        # инициализация обработчиков
        self.handler_commands = HandlerCommands(self.bot)
        self.handler_text_commands = HandlerAllTextCommands(self.bot)
        self.handler_inline_query = HandlerInlineQuery(self.bot)

    def handle(self):
        """ Запуск обработчиков """
        self.handler_commands.handle()
        self.handler_text_commands.handle()
        self.handler_inline_query.handle()

