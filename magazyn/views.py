from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Buty
from .filters import ButyFilter

# Create your views here.
class MagazynListView(PermissionRequiredMixin, ListView):
    model = Buty
    context_object_name = 'buty'
    template_name='magazyn/magazyn_list.html'
    permission_required="magazyn.magazyn_admin"
    
    def get_queryset(self):
        qs = self.model.objects.all()
        my_filter = ButyFilter(self.request.GET, queryset=qs)
        return my_filter.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_filter"] = ButyFilter()
        return context
    
 
class MagazynDetailView(PermissionRequiredMixin, DetailView):
    model = Buty
    context_object_name = 'para'
    template_name='magazyn/magazyn_detail.html'
    permission_required="magazyn.magazyn_admin"


class MagazynCreateView(PermissionRequiredMixin, CreateView):
    model = Buty
    fields = "__all__"
    template_name='magazyn/magazyn_create.html'
    permission_required="magazyn.magazyn_admin"


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