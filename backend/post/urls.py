from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostView.as_view(), name= 'posts_list'),
    path('predict/', views.PredictView.as_view(), name="predict"),

]