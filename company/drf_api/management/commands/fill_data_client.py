from drf_api.models import *
from django.core.management.base import BaseCommand, CommandError
import secrets
import string
import random


class Command(BaseCommand):
    help = 'Создание клиентов'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MAX_LIMIT_USERS = 3

    def handle(self, *args, **options):
        count_iters = 0
        self.stdout.write(f"Начало создание Физ. лиц, Лимит {self.MAX_LIMIT_USERS}")
        for count in range(self.MAX_LIMIT_USERS):
            user = self.create_user(count)
            client = self.crete_client(user)
            self.stdout.write(f"Пользователь успешно создан! {client}")
            count_iters += 1
        self.stdout.write(f"Клиенты успешно созданы, кол-во итераций {count_iters}")

    def crete_client(self, user) -> None:
        client = Client.objects.create(
            user = user,
            type = self.set_type(),
            phone_number = self.set_phone()
        )

        self.set_social_network(
            self.get_randome_social_network(),
            client
        )
        return client

    def get_randome_social_network(self) -> SocialNetworks:
        """
        Добавление 2 соц сети рандомно
        """
        social_network = SocialNetworks.objects.all()
        return [random.choice(social_network), 
                random.choice(social_network)]

    def set_social_network(self, sotial_network_id: list, client: Client) -> None:
        """
        Добавление социальной сети
        """
        network = SocialNetworks.objects.filter(id__in = [_.id for _ in sotial_network_id])
        for _ in network:
            SocialNetworksRef.objects.create(
                client = client,
                social_networks = _,
                url = 'test_url'
            )

    def create_user(self, count) -> CustomUser:
        """
        Создание пользователя для клиента
        """
        user = CustomUser.objects.create(
            username = f'user_{count}',
            first_name = self.set_name(count),
            second_name = self.set_second_name(count),
            patronymic = self.set_patronymic(count),
            gender = self.set_gender(),
        )
        email = Email.objects.create(email = self.set_email())
        user.email.add(email)
        user.set_password(self.generate_password())
        user.save()
        return user

    def set_phone(self) -> str:
        """
        Установка пароля
        """
        phone = f'+7{random.randint(900, 999)}{random.randint(100, 999)}{random.randint(10, 99)}{random.randint(10, 99)}'
        return phone

    def set_name(self, id: int) -> str:
        """
        Установка имени
        """
        return f'Тест {id}'

    def set_second_name(self, id: int) -> str:
        """
        Установка фамилии
        """
        return f'Тестовый {id}'

    def set_patronymic(self, id: int) -> str:
        """
        Установка отчества
        """
        return f'Тестович {id}'
    
    def generate_password(self) -> str:
        """
        Установка пароля
        """
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for i in range(10))
        return password

    def set_email(self) -> str:
        """
        Установка почты
        """
        email = ''.join(random.choice(string.ascii_letters) for x in range(7)) + '@gmail.com'
        return email

    def set_type(self) -> str:
        """
        Установка типа пользователя
        """
        type = [_[0] for _ in dict(TYPE_CHOICES).items()]
        return type

    def set_gender(self) -> str:
        """
        Установка гендора
        """
        genders = [_[0] for _ in dict(GENDER_CHOICES).items()]
        return genders