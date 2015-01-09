'''Models for Pammy'''
from django.db import models
from django.dispatch import receiver

from .fields import IPNetworkField

class Allocation(models.Model):

    name = models.CharField(max_length=500, unique=True)
    network = IPNetworkField(unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subnets')

    def save(self, *args, **kwargs):
        try:
            parents = Allocation.objects.filter(network__is_supernet_of=self.network)
            if self.pk:
                parents = parents.exclude(pk=self.pk)
            self.parent = parents.order_by('-network')[0]
        except IndexError:
            self.parent = None
        super(Allocation, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.network)

@receiver(models.signals.post_save, sender=Allocation)
def shuffle_parents(sender, **kwargs):
    instance = kwargs['instance']
    children = Allocation.objects.filter(network__is_subnet_of=instance.network, parent=instance.parent).exclude(pk=instance.pk)
    children.update(parent=instance)
