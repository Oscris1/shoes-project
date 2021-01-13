from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Buty
from .filters import ButyFilter

# Create your views here.
class MagazynListView(ListView):
    model = Buty
    context_object_name = 'buty'
    template_name='magazyn_list.html'
    
    def get_queryset(self):
        qs = self.model.objects.all()
        my_filter = ButyFilter(self.request.GET, queryset=qs)
        return my_filter.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_filter"] = ButyFilter()
        return context
    
 
class MagazynDetailView(DetailView):
    model = Buty
    context_object_name = 'para'
    template_name='magazyn_detail.html'


class MagazynCreateView(PermissionRequiredMixin, CreateView):
    model = Buty
    fields = "__all__"
    template_name='magazyn_create.html'
    permission_required="magazyn.magazyn_admin"


class MagazynUpdateView(UpdateView):
    model = Buty
    template_name='magazyn_update.html'
    fields = ['status','szacowana_wartosc', 'uwagi', 'data_sprzedazy', 'cena_sprzedazy']


class MagazynDeleteView(DeleteView):
    model = Buty
    context_object_name = 'para'
    template_name='magazyn_delete.html'
    success_url = reverse_lazy('magazyn_list')