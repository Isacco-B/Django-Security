from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.ColumnListView.as_view(), name="column-list"),
    path("create/column", views.ColumnCreateView.as_view(), name="create-column"),
    path(
        "moderator/post", views.ModeratorListView.as_view(), name="moderator-post-list"
    ),
    path(
        "moderator/posts/<pk>/mark-as-public",
        views.ModeratorMarkAsPublic.as_view(),
        name="mark-as-public",
    ),
    path("column/<pk>", views.ColumnDetailView.as_view(), name="column-detail"),
    path("post/<int:pk>", views.PostDetailView.as_view(), name="post-detail"),
    path("create/post", views.PostCreateView.as_view(), name="create-post"),
]
