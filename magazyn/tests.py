from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse

from .models import (
    Marka,
    ModelButa,
    Buty,
    Sprzedane,
    Zwrot,
)

# Create your tests here.
class MagazynTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        cls.super_user = get_user_model().objects.create_superuser(
            email='super_user@email.com',
            username='super_user',
            password='testpass123',
        )
        
        cls.special_user = get_user_model().objects.create_user(
            email='special_user@email.com',
            username='special_user',
            password='testpass123',
        ) 
        cls.special_user.user_permissions.add(Permission.objects.get(codename='magazyn_admin'))

        cls.standard_user = get_user_model().objects.create_user(
            email='standard_user@email.com',
            username='standard_user',
            password='testpass123',
        )
        
        cls.marka = Marka.objects.create(
            name = 'Adidas',
        )

        cls.model_buta = ModelButa.objects.create(
            marka = cls.marka,
            name = 'Yeezy',
        )

        cls.buty = Buty.objects.create(
            marka = cls.marka,
            model_buta = cls.model_buta,
            typ = 'Zebra',
            rozmiar = '45 1/3',
            data_zakupu='2021-01-09',
            cena_zakupu=200,
            szacowana_wartosc=500,
            uwagi='brak',
            status="W magazynie",
            gdzie_kupione='AdidasApp',
        )

        cls.sprzedane = Sprzedane.objects.create(
            buty=cls.buty,
            data_sprzedazy='2021-01-19',
            cena_sprzedazy='490',
            komu_sprzedane='Andrzej',
            wplynely_pieniadze=True,
            data_przesylki='2021-01-23',
            sledzenie_przesylki='https://www.dhl.com/pl-pl/home.html',
        )

        cls.zwrot = Zwrot.objects.create(
            buty= cls.buty,
            data_zwrotu='2021-01-21',
            wplynely_pieniadze=True,
            data_przesylki='2021-01-23',
            sledzenie_przesylki='https://www.dhl.com/pl-pl/home.html',
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
        self.assertEqual(f'{self.buty.rozmiar}', '45 1/3'),
        self.assertEqual(f'{self.buty.data_zakupu}', '2021-01-09'),
        self.assertEqual(f'{self.buty.cena_zakupu}', '200'),
        self.assertEqual(f'{self.buty.szacowana_wartosc}', '500'),
        self.assertEqual(f'{self.buty.uwagi}', 'brak'),
        self.assertEqual(f'{self.buty.status}', 'W magazynie'),
        self.assertEqual(f'{self.buty.gdzie_kupione}', 'AdidasApp'),
        self.assertEqual(f'{self.buty.sprzedane.data_sprzedazy}', '2021-01-19'),
        self.assertEqual(f'{self.buty.sprzedane.cena_sprzedazy}', '490'),

    def test_sprzedane_listening(self):
        self.assertEqual(f'{self.sprzedane.buty.marka.name}', 'Adidas'),
        self.assertEqual(f'{self.sprzedane.data_sprzedazy}', '2021-01-19'),
        self.assertEqual(f'{self.sprzedane.cena_sprzedazy}', '490'),
        self.assertEqual(f'{self.sprzedane.komu_sprzedane}', 'Andrzej'),
        self.assertEqual(f'{self.sprzedane.wplynely_pieniadze}', 'True'),
        self.assertEqual(f'{self.sprzedane.data_przesylki}', '2021-01-23'),
        self.assertEqual(f'{self.sprzedane.sledzenie_przesylki}', 'https://www.dhl.com/pl-pl/home.html'),

    def test_zwrot_listening(self):
        self.assertEqual(f'{self.zwrot.buty.marka.name}', 'Adidas'),
        self.assertEqual(f'{self.zwrot.data_zwrotu}', '2021-01-21'),
        self.assertEqual(f'{self.zwrot.wplynely_pieniadze}', 'True'),
        self.assertEqual(f'{self.zwrot.data_przesylki}', '2021-01-23'),
        self.assertEqual(f'{self.zwrot.sledzenie_przesylki}', 'https://www.dhl.com/pl-pl/home.html'),

    # Testy widoków:

    # Magazyn list view tests
    def test_magazyn_list_view_access(self):
        response = self.client.get(reverse('magazyn_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=('/accounts/login/?next=/magazyn/'))

    def test_magazyn_list_view_access_standard_user(self):
        self.client.login(email='standard_user@email.com', password='testpass123')
        response = self.client.get(reverse('magazyn_list'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_magazyn_list_view_access_special_user(self):
        self.client.login(email='special_user@email.com', password='testpass123')
        response = self.client.get(reverse('magazyn_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/magazyn_list.html')

    def test_magazyn_list_view_access_super_user(self):
        self.client.login(email='super_user@email.com', password='testpass123')
        response = self.client.get(reverse('magazyn_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/magazyn_list.html')


    # Detail views tests
    def test_magazyn_detail_view_access(self):
        response = self.client.get(self.buty.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=('/accounts/login/?next=/magazyn/1/'))

    def test_magazyn_detail_view_access_standard_user(self):
        self.client.login(email='standard_user@email.com', password='testpass123')
        response = self.client.get(self.buty.get_absolute_url())
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_magazyn_detail_view_access_special_user(self):
        self.client.login(email='special_user@email.com', password='testpass123')
        response = self.client.get(self.buty.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/magazyn_detail.html')

    def test_magazyn_detail_view_access_super_user(self):
        self.client.login(email='super_user@email.com', password='testpass123')
        response = self.client.get(self.buty.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/magazyn_detail.html')


    # Create views tests
    def test_magazyn_create_view_access_no_user(self):
        response = self.client.get(reverse('magazyn_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=('/accounts/login/?next=/magazyn/nowe/'))

    def test_magazyn_create_view_access_standard_user(self):
        self.client.login(email='standard_user@email.com', password='testpass123')
        response = self.client.get(reverse('magazyn_create'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_magazyn_create_view_access_special_user(self):
        self.client.login(email='special_user@email.com', password='testpass123')
        response = self.client.get(reverse('magazyn_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/magazyn_create.html')

    def test_magazyn_create_view_access_super_user(self):
        self.client.login(email='super_user@email.com', password='testpass123')
        response = self.client.get(reverse('magazyn_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/magazyn_create.html')


    # Update views tests
    def test_magazyn_update_view_access_no_user(self):
        response = self.client.get(reverse('magazyn_update', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=('/accounts/login/?next=/magazyn/1/zmiana/'))

    def test_magazyn_update_view_access_standard_user(self):
        self.client.login(email='standard_user@email.com', password='testpass123')
        response = self.client.get(reverse('magazyn_update', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_magazyn_update_view_access_special_user(self):
        self.client.login(email='special_user@email.com', password='testpass123')
        response = self.client.get(reverse('magazyn_update', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/magazyn_update.html')

    def test_magazyn_update_view_access_super_user(self):
        self.client.login(email='super_user@email.com', password='testpass123')
        response = self.client.get(reverse('magazyn_update', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/magazyn_update.html')


    # Delete views tests
    def test_magazyn_delete_view_access_no_user(self):
        response = self.client.get(reverse('magazyn_delete', args=[str(self.buty.pk)]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=('/accounts/login/?next=/magazyn/1/usuwanie/'))
        
    def test_magazyn_delete_view_access_standard_user(self):
        self.client.login(email='standard_user@email.com', password='testpass123')
        response = self.client.get(reverse('magazyn_delete', args=[str(self.buty.pk)]))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_magazyn_delete_view_access_special_user(self):
        self.client.login(email='special_user@email.com', password='testpass123')
        response = self.client.get(reverse('magazyn_delete', args=[str(self.buty.pk)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/magazyn_delete.html')

    def test_magazyn_delete_view_access_super_user(self):
        self.client.login(email='super_user@email.com', password='testpass123')
        response = self.client.get(reverse('magazyn_delete', args=[str(self.buty.pk)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/magazyn_delete.html')

    # Sprzedane list view tests
    def test_sprzedane_list_view_access(self):
        response = self.client.get(reverse('sprzedane_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=('/accounts/login/?next=/magazyn/sprzedane/'))

    def test_sprzedane_list_view_access_standard_user(self):
        self.client.login(email='standard_user@email.com', password='testpass123')
        response = self.client.get(reverse('sprzedane_list'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_sprzedane_list_view_access_special_user(self):
        self.client.login(email='special_user@email.com', password='testpass123')
        response = self.client.get(reverse('sprzedane_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/magazyn_list.html')

    def test_sprzedane_list_view_access_super_user(self):
        self.client.login(email='super_user@email.com', password='testpass123')
        response = self.client.get(reverse('sprzedane_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/magazyn_list.html')

     # Zwrot list view tests
    def test_zwrot_list_view_access(self):
        response = self.client.get(reverse('zwrot_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=('/accounts/login/?next=/magazyn/zwrot/'))

    def test_zwrot_list_view_access_standard_user(self):
        self.client.login(email='standard_user@email.com', password='testpass123')
        response = self.client.get(reverse('zwrot_list'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_zwrot_list_view_access_special_user(self):
        self.client.login(email='special_user@email.com', password='testpass123')
        response = self.client.get(reverse('zwrot_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/magazyn_list.html')

    def test_zwrot_list_view_access_super_user(self):
        self.client.login(email='super_user@email.com', password='testpass123')
        response = self.client.get(reverse('zwrot_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/magazyn_list.html')

     # Dokonaj Zwrotu create view test
    def test_zwrot_create_view_access_no_user(self):
        response = self.client.get(reverse('zwrot_create', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=('/accounts/login/?next=/magazyn/1/zwroc_buty/'))

    def test_zwrot_create_view_access_standard_user(self):
        self.client.login(email='standard_user@email.com', password='testpass123')
        response = self.client.get(reverse('zwrot_create', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_zwrot_create_view_access_special_user(self):
        self.client.login(email='special_user@email.com', password='testpass123')
        response = self.client.get(reverse('zwrot_create', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/zwrot_create.html')

    def test_zwrot_create_view_access_super_user(self):
        self.client.login(email='super_user@email.com', password='testpass123')
        response = self.client.get(reverse('zwrot_create', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/zwrot_create.html')

        # Dokonaj Sprzedaży create view test
    def test_zwrot_sprzedaz_view_access_no_user(self):
        response = self.client.get(reverse('sprzedaz_create', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=('/accounts/login/?next=/magazyn/1/sprzedaj_buty/'))

    def test_zwrot_sprzedaz_view_access_standard_user(self):
        self.client.login(email='standard_user@email.com', password='testpass123')
        response = self.client.get(reverse('sprzedaz_create', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_zwrot_sprzedaz_view_access_special_user(self):
        self.client.login(email='special_user@email.com', password='testpass123')
        response = self.client.get(reverse('sprzedaz_create', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/sprzedaz_create.html')

    def test_zwrot_sprzedaz_view_access_super_user(self):
        self.client.login(email='super_user@email.com', password='testpass123')
        response = self.client.get(reverse('sprzedaz_create', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/sprzedaz_create.html')

    # Zwrot delete views tests
    def test_zwrot_delete_view_access_no_user(self):
        response = self.client.get(reverse('zwrot_delete', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=('/accounts/login/?next=/magazyn/1/anuluj_zwrot/'))
        
    def test_zwrot_delete_view_access_standard_user(self):
        self.client.login(email='standard_user@email.com', password='testpass123')
        response = self.client.get(reverse('zwrot_delete', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_zwrot_delete_view_access_special_user(self):
        self.client.login(email='special_user@email.com', password='testpass123')
        response = self.client.get(reverse('zwrot_delete', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/zwrot_delete.html')

    def test_zwrot_delete_view_access_super_user(self):
        self.client.login(email='super_user@email.com', password='testpass123')
        response = self.client.get(reverse('zwrot_delete', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/zwrot_delete.html')


    # Sprzedaz delete views tests
    def test_sprzedaz_delete_view_access_no_user(self):
        response = self.client.get(reverse('sprzedaz_delete', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=('/accounts/login/?next=/magazyn/1/anuluj_sprzedaz/'))
        
    def test_sprzedaz_delete_view_access_standard_user(self):
        self.client.login(email='standard_user@email.com', password='testpass123')
        response = self.client.get(reverse('sprzedaz_delete', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_sprzedaz_delete_view_access_special_user(self):
        self.client.login(email='special_user@email.com', password='testpass123')
        response = self.client.get(reverse('sprzedaz_delete', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/sprzedaz_delete.html')

    def test_sprzedaz_delete_view_access_super_user(self):
        self.client.login(email='super_user@email.com', password='testpass123')
        response = self.client.get(reverse('sprzedaz_delete', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/sprzedaz_delete.html')

    # Zwrot update views tests
    def test_zwrot_update_view_access_no_user(self):
        response = self.client.get(reverse('zwrot_update', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=('/accounts/login/?next=/magazyn/1/edytuj_zwrot/'))

    def test_zwrot_update_view_access_standard_user(self):
        self.client.login(email='standard_user@email.com', password='testpass123')
        response = self.client.get(reverse('zwrot_update', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_zwrot_update_view_access_special_user(self):
        self.client.login(email='special_user@email.com', password='testpass123')
        response = self.client.get(reverse('zwrot_update', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/zwrot_update.html')

    def test_zwrot_update_view_access_super_user(self):
        self.client.login(email='super_user@email.com', password='testpass123')
        response = self.client.get(reverse('zwrot_update', kwargs={'pk': self.buty.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'magazyn/zwrot_update.html')