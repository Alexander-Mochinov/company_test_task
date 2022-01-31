from drf_api.models import *
from django.core.management.base import BaseCommand, CommandError
import random

class Command(BaseCommand):
    help = 'Создание Юр. лиц'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MAX_LIMIT_ENTITY = 3

    def handle(self, *args, **options):

        count_iters = 0
        self.stdout.write(f"Начало создание Юр. лиц, Лимит {self.MAX_LIMIT_ENTITY}")

        for count in range(self.MAX_LIMIT_ENTITY):
            entity = self.create_legal_entity(count)
            self.stdout.write(f"Юр лицо создано! {entity}")
            count_iters += 1

        self.stdout.write(f"Юр. лица успешно созданы, кол-во итераций {count_iters}")

    def create_legal_entity(self, count: int) -> LegalEntity:
        """
        Создание юр лица
        """
        legal_entity = LegalEntity.objects.create(
            full_name = self.set_full_name(count),
            short_name = self.set_short_name(count),
            INN = self.set_INN(),
            KPP = self.set_KPP(),
        )
        return legal_entity

    def set_full_name(self, count: int) -> str:
        """
        Установка полного имени
        """
        return f'This full name {count}'

    def set_short_name(self, count: int) -> str:
        """
        Установка короткого имени
        """
        return f'This short name {count}'

    def set_KPP(self) -> str:
        """
        Установка КПП
        """
        kpp = ''.join([str({random.randint(1, 100)}) for _ in range(8)])
        return kpp

    def set_INN(self) -> str:
        """
        Установка ИНН
        """
        inn = ''.join([str({random.randint(1, 100)}) for _ in range(9)])
        return inn
