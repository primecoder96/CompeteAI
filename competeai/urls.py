from django.urls import path
from . import views

urlpatterns =[
    path("home",views.home,name="home"),
    path("product",views.describe_product,name="product"),
    path("report", views.report, name="report"),
    path("stats",views.render_stat,name="stats"),
]