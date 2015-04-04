'''Pammy views'''
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages

from netaddr import IPNetwork, IPAddress, AddrFormatError

from ..models import Allocation
from ..forms import AllocationForm

def create_posted_networks(request):
    networks = []
    for key, value in request.POST.items():
        if key.startswith('network_'):
            try:
                _, ip, prefix = key.split('_')
            except ValueError:
                continue
            try:
                ip_address = IPAddress(ip)
                ip_network = IPNetwork(str(ip_address) + '/' + prefix)
            except AddrFormatError:
                continue
            if ip_network[0] != ip_address:
                continue
            networks.append(str(ip_network))
            Allocation(network=ip_network, name=value).save()
    messages.success(request, 'Successfully created the networks {}'.format(', '.join(networks)))

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

def network(request, network):

    allocation = get_object_or_404(Allocation, network=network)

    return render(request, 'pammy/network.html', {
        'allocation': allocation,
    })

def delete(request, network):

    allocation = get_object_or_404(Allocation, network=network)

    delete_subs = 'delete-subnets' in request.POST

    to_delete = []
    if delete_subs:
        to_delete = list(allocation.get_descendants())
    to_delete.append(allocation)

    for x in to_delete:
        x.delete()

    messages.success(request, 'Successfully deleted {}{}'.format(allocation.network, ' and all contained subnets' if delete_subs else ''))

    return HttpResponseRedirect(reverse('pammy/ip_list'))

def divide(request, network):

    allocation = get_object_or_404(Allocation, network=network)

    if request.method == 'POST':
        create_posted_networks(request)
        return HttpResponseRedirect(reverse('pammy/ip_list'))

    divisions = zip(range(allocation.network.prefixlen + 1, 33), [2**x for x in range(1, 33)])

    networks = allocation.divide()

    return render(request, 'pammy/divide.html', {
        'divisions': divisions,
        'allocation': allocation,
        'networks': networks,
    })

def fill(request, network):

    allocation = get_object_or_404(Allocation, network=network)

    if request.method == 'POST':
        create_posted_networks(request)
        return HttpResponseRedirect(reverse('pammy/ip_list'))

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
