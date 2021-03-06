# -*- coding: utf-8 -*-
from django.contrib import admin
from vomito.models import Rule, Category, Player, Drink, Turn, Game


class PlayerInline(admin.TabularInline):
    model = Game.players.through


class RuleAdmin(admin.ModelAdmin):
    list_display = ('description', 'randomizable', 'category', 'mixte', 'nb_players', 'on_proc')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'weighting', 'difficulty')


class GameAdmin(admin.ModelAdmin):
    list_display = ('category', 'current_turn')
    exclude = ('players',)
    inlines = (PlayerInline,)

    actions = ('next_turn',)

    def next_turn(self, request, queryset):
        for game in queryset:
            game.next_turn()
        return


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'sex')


class TurnAdmin(admin.ModelAdmin):
    list_display = ('game', 'rule', 'string')


class DrinkAdmin(admin.ModelAdmin):
    list_display = ('player', 'sip', 'bottom_up')

admin.site.register(Turn, TurnAdmin)
admin.site.register(Drink, DrinkAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Rule, RuleAdmin)
admin.site.register(Category, CategoryAdmin)
