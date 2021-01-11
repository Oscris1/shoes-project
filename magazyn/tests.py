from django.test import TestCase

from .models import Marka, ModelButa, Buty
from django.urls import reverse

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
    # Testy dodawania do bazy danych:
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
    # Testy widoków:
    def test_magazyn_list_view(self):
        response = self.client.get(reverse('magazyn_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Adidas')
        self.assertNotContains(response, 'Tego nie powinno tu być na 100%')
        self.assertTemplateUsed(response, 'magazyn_list.html')

    def test_magazyn_detail_view(self):
        response = self.client.get(self.buty.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Adidas')
        self.assertNotContains(response, 'Tego nie powinno tu być na 100%')
        self.assertTemplateUsed(response, 'magazyn_detail.html')

    def test_magazyn_create_view(self):
        response = self.client.post(reverse('magazyn_create'),{
            'marka': 'Adidas',
            'model_buta' : 'Yeezy',
            'typ' : 'Frozen',
            'kolor' : 'Yellow',
            'rozmiar' : '43 1/3',
            'data_zakupu': '2020-05-09',
            'cena_zakupu': 899,
            'szacowana_wartosc': 1200,
            'uwagi': 'super',
            'status': "W magazynie",
            'gdzie_kupione': 'AdidasApp',
            'data_sprzedazy': '2020-12-19',
            'cena_sprzedazy': '1100',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Adidas')
        self.assertContains(response, 'Yeezy')
        self.assertContains(response, 'Frozen')
        self.assertContains(response, 'Yellow')
        self.assertContains(response, '43 1/3')
        self.assertContains(response, '2020-05-09')
        self.assertContains(response, '899')
        self.assertContains(response, '1200')
        self.assertContains(response, 'AdidasApp')
        self.assertContains(response, '2020-12-19')
        self.assertContains(response, '1100')
        self.assertTemplateUsed(response, 'magazyn_create.html')
        self.assertNotContains(response, "Tego nie powinno tu być!")
