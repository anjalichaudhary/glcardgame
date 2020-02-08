from django.urls import path
from core.views import (CardListView, UserListView,
                        GameView, GameDetailView,
                        DrawCardView)


urlpatterns = [
    path('cards/', CardListView.as_view(), name='cards'),
    path('users/', UserListView.as_view(), name='cards'),
    path('games/', GameView.as_view(), name='cards'),
    path('games/<slug:pk>', GameDetailView.as_view(), name='cards'),
    path('draw_card/', DrawCardView.as_view(), name='cards'),

]
