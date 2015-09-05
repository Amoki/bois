# -*- coding: utf-8 -*-
from django.contrib import admin
from vomito.models import Rule, Next, Category, Player, Drink, Turn, Game


class PlayerInline(admin.TabularInline):
    model = Game.players.through


class RuleInline(admin.TabularInline):
    model = Next.rules.through


class RuleAdmin(admin.ModelAdmin):
    list_display = ('description', 'next', 'category', 'mixte', 'nb_players', 'on_proc')


class NextAdmin(admin.ModelAdmin):
    inlines = (RuleInline,)
    exclude = ('rules',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'weighting', 'difficulty')


class GameAdmin(admin.ModelAdmin):
    list_display = ('category',)
    exclude = ('players',)
    inlines = (PlayerInline,)

    actions = ('next_turn',)

    def next_turn(self, request, queryset):
        for game in queryset:
            game.next_turn()
        return


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'sex')


class TurnAdmin(admin.ModelAdmin):
    list_display = ('game', 'rule', 'string')


class DrinkAdmin(admin.ModelAdmin):
    list_display = ('player', 'sip', 'bottoms_up')

admin.site.register(Turn, TurnAdmin)
admin.site.register(Drink, DrinkAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Rule, RuleAdmin)
admin.site.register(Next, NextAdmin)
admin.site.register(Category, CategoryAdmin)
