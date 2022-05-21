from django_project.telegrambot.adminmanage.models import Place
from asgiref.sync import sync_to_async


@sync_to_async
def get_all_places():
    return Place.objects.all()
