from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search"),
    path("edit/<str:title>", views.edit_page, name="edit"),
    path("wiki/<str:title>", views.get_page, name="title")
]
