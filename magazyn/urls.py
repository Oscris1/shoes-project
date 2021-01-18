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
    AnulujSprzedazDeleteView,
    ZwrotUpdateView,
    SprzedaneUpdateView,
)

urlpatterns = [
    path('', MagazynListView.as_view(), name='magazyn_list'),
    path('nowe/', MagazynCreateView.as_view(), name='magazyn_create'),
    path('<int:pk>/', MagazynDetailView.as_view(), name='magazyn_detail'),
    path('<int:pk>/zmiana/', MagazynUpdateView.as_view(), name='magazyn_update'),
    path('<int:pk>/usuwanie/', MagazynDeleteView.as_view(), name='magazyn_delete'),
    
    # zwrot
    path('zwrot/', ZwrotListView.as_view(), name='zwrot_list'),
    path('<int:pk>/zwroc_buty/', DokonajZwrotuCreateView.as_view(), name='zwrot_create'),
    path('<int:pk>/anuluj_zwrot/', AnulujZwrotDeleteView.as_view(), name='zwrot_delete'),
    path('<int:pk>/edytuj_zwrot/', ZwrotUpdateView.as_view(), name='zwrot_update'),

    # sprzedaż
    path('sprzedane/', SprzedaneListView.as_view(), name='sprzedane_list'),
    path('<int:pk>/sprzedaj_buty/', DokonajSprzedazyCreateView.as_view(), name='sprzedaz_create'),
    path('<int:pk>/anuluj_sprzedaz/', AnulujSprzedazDeleteView.as_view(), name='sprzedaz_delete'),
    path('<int:pk>/edytuj_sprzedaz/', SprzedaneUpdateView.as_view(), name='sprzedaz_update'),
]