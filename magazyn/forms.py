from django.forms import ModelForm, DateInput, Textarea

from .models import Buty, Zwrot, Sprzedane


class ButyCreateForm(ModelForm):
    class Meta:
        model = Buty
        fields = (
            "marka",
            "model_buta",
            "typ",
            "rozmiar",
            "data_zakupu",
            "cena_zakupu",
            "szacowana_wartosc",
            "uwagi",
            "gdzie_kupione",
        )
        widgets = {
            "data_zakupu": DateInput(attrs={"placeholder": "DD.MM.RRRR"}),
            "uwagi": Textarea(attrs={"rows": 4}),
        }


class MagazynUpdateForm(ModelForm):
    class Meta:
        model = Buty
        fields = (
            "szacowana_wartosc",
            "uwagi",
        )
        widgets = {
            "uwagi": Textarea(attrs={"rows": 4}),
        }


class DokonajZwrotuForm(ModelForm):
    class Meta:
        model = Zwrot
        fields = (
            "wplynely_pieniadze",
            "data_przesylki",
            "sledzenie_przesylki",
            "data_zwrotu",
        )
        widgets = {
            "data_przesylki": DateInput(attrs={"placeholder": "DD.MM.RRRR"}),
            "data_zwrotu": DateInput(attrs={"placeholder": "DD.MM.RRRR"}),
        }


class DokonajSprzedazyForm(ModelForm):
    class Meta:
        model = Sprzedane
        fields = (
            "data_sprzedazy",
            "cena_sprzedazy",
            "komu_sprzedane",
            "wplynely_pieniadze",
            "data_przesylki",
            "sledzenie_przesylki",
        )
        widgets = {
            "data_sprzedazy": DateInput(attrs={"placeholder": "DD.MM.RRRR"}),
            "data_przesylki": DateInput(attrs={"placeholder": "DD.MM.RRRR"}),
        }
