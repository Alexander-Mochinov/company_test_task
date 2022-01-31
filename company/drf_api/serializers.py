from dataclasses import field
from http import client
from rest_framework import serializers
from drf_api.models import *



class DepartmentLegalEntityRefSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentLegalEntityRef
        fields = '__all__'



class SocialNetworksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetworks
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        # fields = '__all__'
        exclude = ('personal_id',)


class DepartmentClientRefSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DepartmentClientRef
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    client_departament = DepartmentClientRefSerializer(
        many=True, 
        read_only=True
    )

    get_count_clients = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ('id', 'name', 'parent_department', 'client_departament', 'get_count_clients',)


    def get_count_clients(self, obj):
        """
        Получение кол-во клиентов в департаменте
        """
        return obj.get_count_clients()

class LegalEntitySerializer(serializers.ModelSerializer):

    entity_departament = DepartmentLegalEntityRefSerializer(
        many=True,
        read_only=True
    )

    get_count_departament = serializers.SerializerMethodField()

    class Meta:
        model = LegalEntity
        fields = ('id', 'date_joined', 'date_of_change', 'date_status_change', 
                  'full_name', 'short_name', 'INN','KPP', 'get_count_departament', 
                  'entity_departament', )

    def get_count_departament(self, obj):
        """
        Получение кол-ва допартаментов
        """
        return obj.get_count_departament()