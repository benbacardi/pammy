'''Custom fields for Pammy'''
from django.db import models
from django import forms
from django.core.exceptions import ValidationError

from netaddr import IPNetwork, AddrFormatError

class SupernetOf(models.Lookup):
    lookup_name = 'is_supernet_of'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s >>= %s' % (lhs, rhs), params

class SubnetOf(models.Lookup):
    lookup_name = 'is_subnet_of'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s <<= %s' % (lhs, rhs), params

class IPNetworkFormField(forms.CharField):
    def validate(self, value):
        try:
            IPNetwork(value)
        except AddrFormatError as e:
            raise ValidationError(e)
        super(IPNetworkFormField, self).validate(value)

class IPNetworkField(models.Field):
    description = 'An IP Network (IP address and subnet mask combination)'
    __metaclass__ = models.SubfieldBase

    def db_type(self, connection):
        return 'cidr'

    def to_python(self, value):
        if not value:
            return None
        try:
            return IPNetwork(value)
        except AddrFormatError as e:
            raise ValidationError(e)

    def get_prep_value(self, value):
        if not value:
            return None
        if not isinstance(value, IPNetwork):
            try:
                value = IPNetwork(value)
            except AddrFormatError as e:
                raise ValidationError(e)
        return str(value.cidr)

    def formfield(self, **kwargs):
        defaults = {'form_class': IPNetworkFormField}
        defaults.update(kwargs)
        return super(IPNetworkField, self).formfield(**defaults)

IPNetworkField.register_lookup(SupernetOf)
IPNetworkField.register_lookup(SubnetOf)
