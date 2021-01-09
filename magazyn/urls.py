from django.urls import path
from .views import MagazynListView, MagazynDetailView

urlpatterns = [
    path('', MagazynListView.as_view(), name='magazyn_list'),
    path('<int:pk>/', MagazynDetailView.as_view(), name='magazyn_detail'),
]