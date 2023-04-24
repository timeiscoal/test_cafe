from django.urls import path
from menus import views

urlpatterns = [
    path('', views.AllMenuView.as_view(), name="all_menus"),
    path("pagination/",views.MenuPaginationView.as_view({"get":"list"}),name="pagination"),
    path('user/<int:user_id>/', views.MenuCreateView.as_view()),
    path('<int:menu_id>/user/<int:user_id>/', views.MenuDetailView.as_view(), name="detail_menu"),

    path('<str:menu_name>/', views.MenuSearchView.as_view(), name="search_menu"),

    
]
