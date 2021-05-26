
from django.urls import path

from user import views
urlpatterns = [
    path('', views.index, name='user_index'),
    path('password_change/', views.password_change, name='password_change'),
    path('update/', views.user_update, name='user_update'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_detail/<int:id>', views.order_detail, name='order_detail'),
    path('comments/', views.my_comments, name='my_comments'),
    path('deletecomment/<int:id>', views.user_deletecomment,
         name='user_deletecomment')
]
