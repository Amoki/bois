# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('vomito.views',
    url(r'^players/$', 'players'),
    url(r'^categories/$', 'categories'),
    url(r'^player/$', 'player'),
    url(r'^next-turn/$', 'next_turn'),
    url(r'^last-turn/$', 'last_turn'),
    url(r'^follow/$', 'follow'),
    url(r'^game/$', 'game'),
    url(r'^post-game/$', 'post_game'),
    url(r'^$', 'home'),
)
