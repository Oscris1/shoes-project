from django.db import models
from django.urls import reverse


class Marka(models.Model):

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Marki"

    def __str__(self):
        return self.name


class ModelButa(models.Model):
    marka = models.ForeignKey(
        Marka,
        on_delete=models.PROTECT,
        related_name="model_buta",
    )
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Modele"

    def __str__(self):
        return self.name


class Buty(models.Model):
    STATUS = (
        ("w magazynie", "W magazynie"),
        ("sprzedano", "Sprzedano"),
        ("zwrot", "Zwrot"),
    )
    ROZMIAR = (
        ("35", "35"),
        ("35 1/3", "35 1/3"),
        ("35 1/2", "35 1/2"),
        ("35 2/3", "35 2/3"),
        ("36", "36"),
        ("36 1/3", "36 1/3"),
        ("36 1/2", "36 1/2"),
        ("36 2/3", "36 2/3"),
        ("37", "37"),
        ("37 1/3", "37 1/3"),
        ("37 1/2", "37 1/2"),
        ("37 2/3", "37 2/3"),
        ("38", "38"),
        ("38 1/3", "38 1/3"),
        ("38 1/2", "38 1/2"),
        ("38 2/3", "38 2/3"),
        ("39", "39"),
        ("39 1/3", "39 1/3"),
        ("39 1/2", "39 1/2"),
        ("39 2/3", "39 2/3"),
        ("40", "40"),
        ("40 1/3", "40 1/3"),
        ("40 1/2", "40 1/2"),
        ("40 2/3", "40 2/3"),
        ("41", "41"),
        ("41 1/3", "41 1/3"),
        ("41 1/2", "41 1/2"),
        ("41 2/3", "41 2/3"),
        ("42", "42"),
        ("42 1/3", "42 1/3"),
        ("42 1/2", "42 1/2"),
        ("42 2/3", "42 2/3"),
        ("43", "43"),
        ("43 1/3", "43 1/3"),
        ("43 1/2", "43 1/2"),
        ("43 2/3", "43 2/3"),
        ("44", "44"),
        ("44 1/3", "44 1/3"),
        ("44 1/2", "44 1/2"),
        ("44 2/3", "44 2/3"),
        ("45", "45"),
        ("45 1/3", "45 1/3"),
        ("45 1/2", "45 1/2"),
        ("45 2/3", "45 2/3"),
        ("46", "46"),
        ("46 1/3", "46 1/3"),
        ("46 1/2", "46 1/2"),
        ("46 2/3", "46 2/3"),
        ("47", "47"),
        ("47 1/3", "47 1/3"),
        ("47 1/2", "47 1/2"),
        ("47 2/3", "47 2/3"),
        ("48", "48"),
        ("48 1/3", "48 1/3"),
        ("48 1/2", "48 1/2"),
        ("48 2/3", "48 2/3"),
    )
    marka = models.ForeignKey(Marka, on_delete=models.PROTECT)
    model_buta = models.ForeignKey(
        ModelButa,
        on_delete=models.PROTECT,
    )
    typ = models.CharField(max_length=50)
    rozmiar = models.CharField(max_length=7, choices=ROZMIAR)
    data_zakupu = models.DateField(null=True)
    cena_zakupu = models.DecimalField(max_digits=8, decimal_places=2)
    szacowana_wartosc = models.DecimalField(
        max_digits=8, decimal_places=2, null=True
    )
    uwagi = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=200, choices=STATUS)
    gdzie_kupione = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name_plural = "Buty"

        permissions = [
            ("magazyn_admin", "User can do everything in Magazyn app")
        ]

    def __str__(self):
        return (
            self.marka.name
            + " "
            + self.model_buta.name
            + " id: "
            + str(self.pk)
        )

    def get_absolute_url(self):
        return reverse("magazyn_detail", kwargs={"pk": self.pk})


class BazowaPrzesylka(models.Model):
    BOOL_CHOICES = ((True, "Tak"), (False, "Nie"))
    wplynely_pieniadze = models.BooleanField(
        verbose_name="Wpłynęły pieniądze", choices=BOOL_CHOICES, default=False
    )
    data_przesylki = models.DateField(
        verbose_name="Data przesyłki", null=True, blank=True
    )
    sledzenie_przesylki = models.URLField(
        verbose_name="Link do śledzenia przesyłki", null=True, blank=True
    )

    class Meta:
        abstract = True


class Sprzedane(BazowaPrzesylka):
    buty = models.OneToOneField(
        Buty, on_delete=models.CASCADE, primary_key=True
    )
    data_sprzedazy = models.DateField(null=True, blank=True)
    cena_sprzedazy = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    komu_sprzedane = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Sprzedane"

    def __str__(self):
        return self.buty.__str__()

    def get_absolute_url(self):
        return reverse("magazyn_detail", kwargs={"pk": self.pk})


class Zwrot(BazowaPrzesylka):
    buty = models.OneToOneField(
        Buty, on_delete=models.CASCADE, primary_key=True
    )
    data_zwrotu = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Zwrot"

    def __str__(self):
        return self.buty.__str__()

    def get_absolute_url(self):
        return reverse("magazyn_detail", kwargs={"pk": self.pk})
