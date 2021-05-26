from django.urls import path
from product import views

urlpatterns = [
    path("<int:id>/<str:slug>/", views.product_detail, name="product_detail"),
    path("addlike", views.addlike, name="addlike"),
    path("addcompare", views.addcompare, name="addcompare"),
    path("addcomment/<int:id>", views.addcomment, name="addcomment"),
]
