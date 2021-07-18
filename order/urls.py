from django.urls import path
from order import views

urlpatterns = [
    path("create/", views.order_create, name="order_create"),
    path("created/", views.order_created, name="order_created"),
    path(
        "admin/order/<int:order_id>/",
        views.admin_order_detail,
        name="admin_order_detail",
    ),
    path(
        "admin/order/<int:order_id>/pdf/", views.admin_order_pdf, name="admin_order_pdf"
    ),
    
]
