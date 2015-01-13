'''Pammy API v1'''
from .resources import AllocationResource
from tastypie.api import Api

api = Api(api_name='v1')
api.register(AllocationResource())
