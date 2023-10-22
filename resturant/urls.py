from django.urls import path
from .views import GroupMemeberView

urlpatterns = [
    path("user-group/",GroupMemeberView.as_view()),
    path("user/<int:user_id>/group",GroupMemeberView.as_view()),
    path("user/<int:user_id>/group/<int:group_id>/",GroupMemeberView.as_view()),

]
