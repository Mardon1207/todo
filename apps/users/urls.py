from django.urls import path
from .views import UsersView, UsersItemView


urlpatterns = [
    path('', UsersView.as_view()),
    path('me', UsersItemView.as_view())
]
