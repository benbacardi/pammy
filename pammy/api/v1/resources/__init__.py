'''Pammy API resources'''
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from ....models import Allocation

class AllocationResource(ModelResource):
    subnets = fields.ToManyField('self', 'subnets', null=True, full=True)

    class Meta:
        queryset = Allocation.objects.filter(parent__isnull=True).order_by('network')
        fields = [
            'name',
            'network',
            'pk',
        ]
        filtering = {
            'network': ALL,
            'supernet': ALL_WITH_RELATIONS,
        }
