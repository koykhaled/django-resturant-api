from django.urls import path
from .views import GroupMemeberView,MenuItemsView

urlpatterns = [
    path("user/group",GroupMemeberView.as_view()),
    path("user/<int:user_id>/group/",GroupMemeberView.as_view()),
    path("user/<int:user_id>/group/<int:group_id>/",GroupMemeberView.as_view()),
    # Menu Items 
    path('menu-items/',MenuItemsView.as_view()),
    path('menu-items/<int:item_id>',MenuItemsView.as_view()),

]
