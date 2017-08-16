import os
from paneity.settings_prod import SECRET_KEY
from django_private_chat.management.commands.run_chat_server \
    import Command as RunChatServer


class Command(RunChatServer):

    def handle(self, *args, **options):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'paneity.settings_prod'
        os.environ['DJANGO_SECRET_KEY'] = SECRET_KEY
        super().handle(args, options)
