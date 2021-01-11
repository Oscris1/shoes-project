from django.urls import path
from .views import MagazynListView, MagazynDetailView, MagazynCreateView, MagazynUpdateView

urlpatterns = [
    path('', MagazynListView.as_view(), name='magazyn_list'),
    path('nowe/', MagazynCreateView.as_view(), name='magazyn_create'),
    path('<int:pk>/', MagazynDetailView.as_view(), name='magazyn_detail'),
    path('<int:pk>/zmiana/', MagazynUpdateView.as_view(), name='magazyn_update'),
]