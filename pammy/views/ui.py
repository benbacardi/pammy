'''Pammy UI views'''
from django.shortcuts import render

from ..models import Allocation

def allocation_table(request):
    
    try:
        allocation = Allocation.objects.get(network=request.GET['supernet'])
        allocations = allocation.subnets.all().order_by('network')
    except (Allocation.DoesNotExist, KeyError):
        allocations = Allocation.objects.filter(parent__isnull=True).order_by('network')

    return render(request, 'pammy/allocation_table.html', {
        'allocations': allocations,
    })
