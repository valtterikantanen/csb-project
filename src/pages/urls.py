from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('sign-up', sign_up, name='sign-up'),
    path('login', log_in, name='login'),
    path('logout', log_out, name='logout'),
    path('reviews', reviews, name='reviews'),
    path('reviews/new', new_review, name='new-review'),
    path('reviews/<id>/edit', edit_review, name='edit-review'),
]
