from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from utils.json_renderer import JSONResponse
from utils.required_params import check_params

from vomito.models import Game, Player, Category
from vomito.serializers import PlayerSerializer, TurnSerializer


def home(request):
    categories = Category.objects.all()

    return render(request, 'index.html', locals())


@api_view(['GET'])
def players(request):
    return JSONResponse(PlayerSerializer(Player.objects.all()).data)


@api_view(['POST'])
def post_game(request):
    check_params(request, ['category', 'players'])

    players = Player.objects.find(pk__in=request.data.get('players'))
    category = Player.objects.get(pk=request.data.get('category'))

    male = False
    female = False

    for player in players:
        if player.sex == Player.Male:
            male = True
        else:
            female = True

    game = Game(category=category, mixte=(male and female))
    game.save()
    game.players.add(*players)

    request.session['game'] = game.pk

    return redirect('game')


@api_view(['GET'])
def game(request):
    if not request.session.get('game', False):
        return redirect('home')

    return render(request, 'game')


@api_view(['POST'])
def player(request):
    check_params('first_name', 'last_name', 'sex')
    player = Player(
        first_name=request.data.get('first_name'),
        last_name=request.data.get('last_name'),
        sex=request.data.get('sex'),
    )
    player.save()
    return JSONResponse(PlayerSerializer(player).data)


@api_view(['GET'])
def last_turn(request):
    if not request.session.get('game', False):
        return redirect('home')

    turn = Game.objects.get(pk=request.session['game']).turn_set.last()
    return JSONResponse(TurnSerializer(turn).data)


@api_view(['POST'])
def next_turn(request):
    if not request.session.get('game', False):
        return redirect('home')

    game = Game.objects.get(pk=request.session['game'])
    game.next_turn()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def follow(request):
    check_params('game')

    return render(request, 'follow', {game: request.data.get('game')})
