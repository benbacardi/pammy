'''Pammy API v1'''
from .resources import AllocationResource, AllocationResource0
from tastypie.api import Api

api = Api(api_name='v1')
api.register(AllocationResource())

api0 = Api(api_name='v0')
api0.register(AllocationResource0())
