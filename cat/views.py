from rest_framework import viewsets
from .models import SpyCat
from .serializers import SpyCatSerializer

class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer