from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from utils.check_params import check_params

from vomito.models import Game, Player, Category, Turn
from vomito.serializers import PlayerSerializer, TurnSerializer, CategorySerializer


@api_view(['GET'])
def home(request):
    categories = Category.objects.all()

    return render(request, 'index.html', locals())


@api_view(['GET'])
def players(request):
    return Response(PlayerSerializer(Player.objects.all(), many=True).data)


@api_view(['GET'])
def categories(request):
    return Response(CategorySerializer(Category.objects.all(), many=True).data)


@api_view(['POST'])
def post_game(request):
    check_params(request, ['category', 'players'])

    players = Player.objects.filter(pk__in=request.data.get('players'))
    category = Category.objects.get(pk=request.data.get('category'))

    male = False
    female = False

    for player in players:
        if player.sex == Player.MALE:
            male = True
        else:
            female = True

    game = Game(category=category, mixte=(male and female))
    game.save()
    game.players.add(*players)

    request.session['game'] = game.pk

    return redirect('/game')


@api_view(['GET'])
def game(request):
    if not request.session.get('game', False):
        return redirect('home')

    return render(request, 'game.html')


@api_view(['POST'])
def player(request):
    check_params(request, ('first_name', 'sex'))

    player = Player(
        first_name=request.data.get('first_name'),
        sex=request.data.get('sex'),
    )
    player.save()
    return Response(PlayerSerializer(player).data)


@api_view(['GET'])
def last_turn(request):
    if not request.session.get('game', False):
        return redirect('home')

    game = Game.objects.get(pk=request.session['game'])

    turn = Turn.objects.get(game=game, number=game.turn_number)
    return Response(TurnSerializer(turn).data)


@api_view(['POST'])
def next_turn(request):
    if not request.session.get('game', False):
        return redirect('home')

    game = Game.objects.get(pk=request.session['game'])
    game.next_turn()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def follow(request):
    check_params(request, ('game',))

    return render(request, 'follow.html', {game: request.data.get('game')})
