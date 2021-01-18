from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Buty, Zwrot, Sprzedane
from .filters import ButyFilter

# Create your views here.
class MagazynListView(PermissionRequiredMixin, ListView):
    model = Buty
    context_object_name = 'buty'
    template_name='magazyn/magazyn_list.html'
    permission_required="magazyn.magazyn_admin"
    
    def get_queryset(self):
        qs = super().get_queryset().filter(status='w magazynie')
        #self.model.objects.all()
        my_filter = ButyFilter(self.request.GET, queryset=qs)
        return my_filter.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_filter"] = ButyFilter()
        context["list_header"] = "Lista butów"
        return context
    
 
class MagazynDetailView(PermissionRequiredMixin, DetailView):
    model = Buty
    context_object_name = 'para'
    template_name='magazyn/magazyn_detail.html'
    permission_required="magazyn.magazyn_admin"


class MagazynCreateView(PermissionRequiredMixin, CreateView):
    model = Buty
    fields = [
        'marka', 
        'model_buta', 
        'typ', 
        'rozmiar', 
        'data_zakupu', 
        'cena_zakupu', 
        'szacowana_wartosc', 
        'uwagi', 
        'gdzie_kupione',
        ]
    template_name='magazyn/magazyn_create.html'
    permission_required="magazyn.magazyn_admin"

    def form_valid(self, form):
        form.instance.status = "w magazynie"
        return super().form_valid(form)


class MagazynUpdateView(PermissionRequiredMixin, UpdateView):
    model = Buty
    context_object_name = 'para'
    template_name='magazyn/magazyn_update.html'
    fields = ['status','szacowana_wartosc', 'uwagi',] #'data_sprzedazy', 'cena_sprzedazy'
    permission_required="magazyn.magazyn_admin"


class MagazynDeleteView(PermissionRequiredMixin, DeleteView):
    model = Buty
    context_object_name = 'para'
    template_name='magazyn/magazyn_delete.html'
    success_url = reverse_lazy('magazyn_list')
    permission_required="magazyn.magazyn_admin"


class SprzedaneListView(PermissionRequiredMixin, ListView):
    model = Buty
    context_object_name = 'buty'
    template_name='magazyn/magazyn_list.html'
    permission_required="magazyn.magazyn_admin"
    
    def get_queryset(self):
        qs = super().get_queryset().filter(status='sprzedano')
        my_filter = ButyFilter(self.request.GET, queryset=qs)
        return my_filter.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_filter"] = ButyFilter()
        context["list_header"] = "Sprzedane buty"
        return context


class ZwrotListView(PermissionRequiredMixin, ListView):
    model = Buty
    context_object_name = 'buty'
    template_name='magazyn/magazyn_list.html'
    permission_required="magazyn.magazyn_admin"
    
    def get_queryset(self):
        qs = super().get_queryset().filter(status='zwrot')
        my_filter = ButyFilter(self.request.GET, queryset=qs)
        return my_filter.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_filter"] = ButyFilter()
        context["list_header"] = "Zwrócone buty"
        return context


class DokonajZwrotuCreateView(PermissionRequiredMixin, CreateView):
    model = Zwrot
    fields = [
        'wplynely_pieniadze', 
        'data_przesylki', 
        'sledzenie_przesylki', 
        'data_zwrotu',
        ]
    context_object_name = 'zwrot'
    template_name='magazyn/zwrot_create.html'
    permission_required="magazyn.magazyn_admin"

    def form_valid(self, form):
        form.instance.pk = self.kwargs['pk'] # set new Zwrot object pk to given pk
        
        # change buty status to "zwrot" on create Zwrot object
        buty = Buty.objects.get(pk=self.kwargs['pk'])
        buty.status='zwrot'
        buty.save()
        return super().form_valid(form)


class AnulujZwrotDeleteView(PermissionRequiredMixin, DeleteView):
    model = Zwrot
    context_object_name = 'para'
    template_name='magazyn/zwrot_delete.html'
    permission_required="magazyn.magazyn_admin"

    def get_success_url(self):
        # redirect to shoes detail page
        return reverse_lazy ('magazyn_detail', kwargs={'pk': self.kwargs['pk']})

    def delete(self, request, *args, **kwargs):
        # change buty status to "w magazynie" on delete
        buty = Buty.objects.get(pk=self.kwargs['pk'])
        buty.status='w magazynie'
        buty.save()
        return super().delete(request, *args, **kwargs)


class DokonajSprzedazyCreateView(PermissionRequiredMixin, CreateView):
    model = Sprzedane
    fields = [
        'data_sprzedazy',
        'cena_sprzedazy',
        'komu_sprzedane', 
        'wplynely_pieniadze', 
        'data_przesylki', 
        'sledzenie_przesylki',
        ]
    context_object_name = 'zwrot'
    template_name='magazyn/sprzedaz_create.html'
    permission_required="magazyn.magazyn_admin"

    def form_valid(self, form):
        form.instance.pk = self.kwargs['pk']  # set new Sprzedane object pk to given pk
        
        # change buty status to "sprzedano" on create Sprzedane object
        buty = Buty.objects.get(pk=self.kwargs['pk'])
        buty.status='sprzedano'
        buty.save()
        return super().form_valid(form)


class AnulujSprzedazDeleteView(PermissionRequiredMixin, DeleteView):
    model = Sprzedane
    context_object_name = 'para'
    template_name='magazyn/sprzedaz_delete.html'
    permission_required="magazyn.magazyn_admin"

    def get_success_url(self):
        # redirect to shoes detail page
        return reverse_lazy ('magazyn_detail', kwargs={'pk': self.kwargs['pk']})

    def delete(self, request, *args, **kwargs):
        # change buty status to "sprzedano" on delete
        buty = Buty.objects.get(pk=self.kwargs['pk'])
        buty.status='w magazynie'
        buty.save()
        return super().delete(request, *args, **kwargs)
