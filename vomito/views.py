from django.shortcuts import render

from vomito.models import Game, Player, Category


def home(request):
    categories = Category.objects.all()

    return render(request, 'index.html', locals())


