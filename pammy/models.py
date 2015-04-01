'''Models for Pammy'''
from django.db import models
from django.dispatch import receiver

from closuretree.models import ClosureModel

from .fields import IPNetworkField
from .utils import subnet_complement

class Allocation(ClosureModel):

    name = models.CharField(max_length=500, unique=True)
    network = IPNetworkField(unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subnets', on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        try:
            parents = Allocation.objects.filter(network__is_supernet_of=self.network)
            if self.pk:
                parents = parents.exclude(pk=self.pk)
            self.parent = parents.order_by('-network')[0]
        except IndexError:
            self.parent = None
        super(Allocation, self).save(*args, **kwargs)

    def complement(self):
        return subnet_complement(self.network, [x.network for x in self.subnets.all()])

    def __str__(self):
        return str(self.network)

    class ClosureMeta:
        parent_attr = 'parent'

@receiver(models.signals.pre_delete, sender=Allocation)
def shuffle_parents_on_delete(sender, **kwargs):
    instance = kwargs['instance']
    instance.subnets.update(parent=instance.parent)

@receiver(models.signals.post_save, sender=Allocation)
def shuffle_parents_on_save(sender, **kwargs):
    instance = kwargs['instance']
    children = Allocation.objects.filter(network__is_subnet_of=instance.network, parent=instance.parent).exclude(pk=instance.pk)
    children.update(parent=instance)
