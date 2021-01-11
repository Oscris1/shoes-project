from django.urls import path
from .views import MagazynListView, MagazynDetailView, MagazynCreateView

urlpatterns = [
    path('', MagazynListView.as_view(), name='magazyn_list'),
    path('nowe/', MagazynCreateView.as_view(), name='magazyn_create'),
    path('<int:pk>/', MagazynDetailView.as_view(), name='magazyn_detail'),
]