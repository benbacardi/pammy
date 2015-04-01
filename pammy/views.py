'''Pammy views'''
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy

from .models import Allocation
from .forms import AllocationForm

def ip_list(request):
    return render(request, 'pammy/ip_list.html', {
        'allocations': Allocation.objects.filter(parent__isnull=True).order_by('network'),
    })


class AllocationFormView(FormView):
    template_name = 'add_allocation.html'
    form_class = AllocationForm
    success_url = reverse_lazy('pammy.views.ip_list')
