from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="inventory-index"),
    path("create", views.create, name="inventory-create"),
    path("detail/<int:product_id>", views.detail, name="inventory-detail"),
    path("update/<int:product_id>", views.update, name="inventory-update"),
    path("delete/<int:product_id>", views.delete, name="inventory-delete"),
    path("download", views.download, name="inventory-download"),
    # path("create_dummy_data", views.create_dummy_data, name="inventory-dummy"),
]
