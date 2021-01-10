from django.test import TestCase

from .models import Marka, ModelButa, Buty

# Create your tests here.
class MagazynTests(TestCase):

    def setUp(self):
        self.marka = Marka.objects.create(
            name = 'Adidas',
        )

        self.model_buta = ModelButa.objects.create(
            marka = self.marka,
            name = 'Yeezy',
        )

        self.buty = Buty.objects.create(
            marka = self.marka,
            model_buta = self.model_buta,
            typ = 'Zebra',
            kolor = 'White',
            rozmiar = '45 1/3',
            data_zakupu='2021-01-09',
            cena_zakupu=200,
            szacowana_wartosc=500,
            uwagi='brak',
            status="W magazynie",
            gdzie_kupione='AdidasApp',
            data_sprzedazy='2021-01-19',
            cena_sprzedazy='490',
        )

    def test_marka_listening(self):
        self.assertEqual(f'{self.marka.name}', 'Adidas'),

    def test_model_buta_listening(self):
        self.assertEqual(f'{self.model_buta.marka.name}', 'Adidas'),
        self.assertEqual(f'{self.model_buta.name}', 'Yeezy'),

    def test_buty_listening(self):
        self.assertEqual(f'{self.buty.marka.name}', 'Adidas'),
        self.assertEqual(f'{self.buty.model_buta.name}', 'Yeezy'),
        self.assertEqual(f'{self.buty.typ}', 'Zebra'),
        self.assertEqual(f'{self.buty.kolor}', 'White'),
        self.assertEqual(f'{self.buty.rozmiar}', '45 1/3'),
        self.assertEqual(f'{self.buty.data_zakupu}', '2021-01-09'),
        self.assertEqual(f'{self.buty.cena_zakupu}', '200'),
        self.assertEqual(f'{self.buty.szacowana_wartosc}', '500'),
        self.assertEqual(f'{self.buty.uwagi}', 'brak'),
        self.assertEqual(f'{self.buty.status}', 'W magazynie'),
        self.assertEqual(f'{self.buty.gdzie_kupione}', 'AdidasApp'),
        self.assertEqual(f'{self.buty.data_sprzedazy}', '2021-01-19'),
        self.assertEqual(f'{self.buty.cena_sprzedazy}', '490'),
