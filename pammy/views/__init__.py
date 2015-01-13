'''Pammy views'''
from django.shortcuts import render

from ..models import Allocation

def ip_list(request):

    return render(request, 'pammy/ip_list.html', {
        'allocations': Allocation.objects.filter(parent__isnull=True).order_by('network'),
    })
