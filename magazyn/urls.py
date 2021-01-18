from django.urls import path
from .views import (
    MagazynListView, 
    MagazynDetailView, 
    MagazynCreateView, 
    MagazynUpdateView, 
    MagazynDeleteView,
    SprzedaneListView,
    ZwrotListView,
    DokonajZwrotuCreateView,
    DokonajSprzedazyCreateView,
    AnulujZwrotDeleteView,
)

urlpatterns = [
    path('', MagazynListView.as_view(), name='magazyn_list'),
    path('sprzedane/', SprzedaneListView.as_view(), name='sprzedane_list'),
    path('zwrot/', ZwrotListView.as_view(), name='zwrot_list'),
    path('nowe/', MagazynCreateView.as_view(), name='magazyn_create'),
    path('<int:pk>/', MagazynDetailView.as_view(), name='magazyn_detail'),
    path('<int:pk>/zmiana/', MagazynUpdateView.as_view(), name='magazyn_update'),
    path('<int:pk>/usuwanie/', MagazynDeleteView.as_view(), name='magazyn_delete'),
    path('<int:pk>/zwroc_buty/', DokonajZwrotuCreateView.as_view(), name='zwrot_create'),
    path('<int:pk>/anuluj_zwrot/', AnulujZwrotDeleteView.as_view(), name='anuluj_zwrot'),
    path('<int:pk>/sprzedaj_buty/', DokonajSprzedazyCreateView.as_view(), name='sprzedaz_create'),
]