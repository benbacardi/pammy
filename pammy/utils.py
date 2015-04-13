'''Pammy utils'''
from django.utils.http import urlencode
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from django.utils import six

def subnet_complement(supernet, existing_subnets):
    '''Return the complement of subnets for the given supernet and it's existing subnets'''
    for possible_subnet in supernet.subnet(supernet.prefixlen + 1):
        if any(possible_subnet in current_subnet for current_subnet in existing_subnets):
            continue
        elif any(current_subnet in possible_subnet for current_subnet in existing_subnets):
            for subnet in subnet_complement(possible_subnet, existing_subnets):
                yield subnet
        else:
            yield possible_subnet

def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    '''Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search', 'Bob'})
    '''
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url

reverse_querystring_lazy = lazy(reverse_querystring, str)
