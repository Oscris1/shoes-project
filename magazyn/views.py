from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView 
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


class MagazynCreateView(CreateView):
    model = Buty
    fields = "__all__"
    template_name='magazyn_create.html'