from xmlrpc import client
from drf_api.models import *
from django.core.management.base import BaseCommand, CommandError
import random

class Command(BaseCommand):

    help = 'Создание Департамента'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MAX_LIMIT_DEPARTAMENT = 3

    def handle(self, *args, **options):
        count_iters = 0
        self.stdout.write(f"Начало создание Департамента, Лимит {self.MAX_LIMIT_DEPARTAMENT}")

        for count in range(self.MAX_LIMIT_DEPARTAMENT):
            departament = self.create_legal_entity(count)
            self.stdout.write(f"Департамент создано! {departament}")
            count_iters += 1

        self.stdout.write(f"Департаменты успешно созданы, кол-во итераций {count_iters}")

        self.set_clients_in_departament()
        self.set_entity_in_departament()

    def create_departament(self, count: int) -> LegalEntity:
        """
        Создание департамента
        """
        departament = Department.objects.create(
           name = self.set_name(count)
        )
        return departament

    def set_name(self, count: int) -> str:
        """
        Установка имени
        """
        return f'This full name departament {count}'

    def set_entity_in_departament(self) -> None:
        """
        Установка Юр лиц в депортаменты
        """
        legal_entity = LegalEntity.objects.all()
        departament = Department.objects.all()
        for _ in departament:
            DepartmentLegalEntityRef.objects.create(
                department = _,
                legal_entity = random.choice(legal_entity)
            )
    
    def set_clients_in_departament(self) -> None:
        """
        Установка клиентов в депортаменты
        """
        clients = Client.objects.all()
        departament = Department.objects.all()
        for _ in departament:
            DepartmentClientRef.objects.create(
                department = _,
                client = random.choice(clients)
            )        