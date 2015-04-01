'''Pammy views'''
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages

from ..models import Allocation
from ..forms import AllocationForm

def ip_list(request):

    if 'supernet' in request.GET:
        allocations = Allocation.objects.filter(network=request.GET['supernet'])
    else:
        allocations = Allocation.objects.filter(parent__isnull=True).order_by('network')

    if request.method == 'POST':
        new_allocation = AllocationForm(request.POST)
        if new_allocation.is_valid():
            allocation = new_allocation.save()
            messages.success(request, 'Subnet {} created successfully.'.format(allocation))
            return HttpResponseRedirect('.')
    else:
        new_allocation = AllocationForm()

    return render(request, 'pammy/ip_list.html', {
        'new_allocation': new_allocation,
        'allocations': allocations,
    })

def divide(request, network):

    allocation = get_object_or_404(Allocation, network=network)

    return render(request, 'pammy/divide.html', {
        'allocation': allocation,
    })

def fill(request, network):

    allocation = get_object_or_404(Allocation, network=network)
    complement = list(allocation.complement())

    if not complement:
        messages.warning(request, 'There are no gaps to fill in {}'.format(allocation.network))
        return HttpResponseRedirect(reverse('pammy/ip_list'))

    complements = [(x, None) for x in complement]
    existing = [(x.network, x) for x in allocation.subnets.all()]
    all_networks = sorted(complements + existing, key=lambda x: x[0])

    return render(request, 'pammy/fill.html', {
        'allocation': allocation,
        'networks': all_networks,
    })
