'''Pammy UI views'''
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from netaddr import IPNetwork, AddrFormatError

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

def split_network(request):

    try:
        network = IPNetwork(request.GET['network'])
    except (KeyError, AddrFormatError):
        return HttpResponseBadRequest()

    return render(request, 'pammy/split_network.html', {
        'networks': network.subnet(network.prefixlen + 1),
    })
