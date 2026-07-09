from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

