'''Models for Pammy'''
from django.db import models
from django.dispatch import receiver

from closuretree.models import ClosureModel

from .fields import IPNetworkField
from .utils import subnet_complement

class Allocation(ClosureModel):

    name = models.CharField(max_length=500)
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

    @property
    def full(self):
        try:
            self.complement().next()
            return False
        except StopIteration:
            return True

    def fully_divided(self):
        networks = list(self.network.subnet(self.network.prefixlen + 1))
        return len(networks) == Allocation.objects.filter(network__in=networks).count()

    def complement(self):
        return subnet_complement(self.network, [x.network for x in self.subnets.all()])

    def divide(self, prefixlen=None):
        if prefixlen is None:
            prefixlen = self.network.prefixlen + 1
        subnets = list(self.subnets.order_by('network'))
        subnet_networks = [x.network for x in subnets]
        networks = []
        for subnet in self.network.subnet(prefixlen):
            #if subnet in subnet_networks:
                #continue
            contains = [x for x in subnets if x.network in subnet]
            networks.append((subnet, contains))
        return networks

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
