import django_filters
from .models import Buty


class ButyFilter(django_filters.FilterSet):
    class Meta:
        model = Buty
        fields = ['marka', 'model_buta', 'rozmiar']