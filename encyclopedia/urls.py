from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="title"),
    path("new", views.new, name="new"),
    path("random", views.rand_entry, name="random"),
    path("<str:edit>", views.edit, name="edit")
]
