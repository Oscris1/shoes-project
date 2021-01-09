from django.views.generic import ListView, DetailView
from .models import Buty

# Create your views here.
class MagazynListView(ListView):
    model = Buty
    context_object_name = 'buty'
    template_name='magazyn_list.html'


class MagazynDetailView(DetailView):
    model = Buty
    context_object_name = 'para'
    template_name='magazyn_detail.html'