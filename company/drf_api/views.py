from drf_api.models import CustomUser
from django.shortcuts import get_object_or_404
from drf_api.serializers import *
from rest_framework import viewsets
from rest_framework.response import responses
from rest_framework import generics, views, status, parsers
from rest_framework.response import Response

class SocialNetworksViewSet(viewsets.ModelViewSet):
    serializer_class = SocialNetworksSerializer
    queryset = SocialNetworks.objects.all()
    parser_classes = (parsers.MultiPartParser,)


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    parser_classes = (parsers.MultiPartParser,)


class LegalEntityViewSet(viewsets.ModelViewSet):
    serializer_class = LegalEntitySerializer
    queryset = LegalEntity.objects.all()
    parser_classes = (parsers.MultiPartParser,)

class DepartmentLegalEntityRefViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentLegalEntityRefSerializer
    queryset = DepartmentLegalEntityRef.objects.all()
    parser_classes = (parsers.MultiPartParser,)


class DepartmentClientRefViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentClientRefSerializer
    queryset = DepartmentClientRef.objects.all()
    parser_classes = (parsers.MultiPartParser,)


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    parser_classes = (parsers.MultiPartParser,)