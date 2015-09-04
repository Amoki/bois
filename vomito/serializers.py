# -*- coding: utf-8 -*-

from rest_framework import serializers

from vomito.models import Player, Turn


class PlayerSerializer(serializers.ModelSerializer):
    """
    Serializing all the Player
    """

    class Meta:
        model = Player
        fields = ('pk', 'first_name', 'last_name', 'sex')


class TurnSerializer(serializers.ModelSerializer):
    """
    Serializing all the Turn
    """

    class Meta:
        model = Turn
        fields = ('string')
