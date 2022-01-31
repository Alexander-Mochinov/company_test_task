from drf_api.models import Email, CustomUser
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Создание администратора'

    def handle(self, *args, **options):
        email = str(input('--> Установка почты: ').strip())
        username = str(input('--> Установка логина: ').strip())
        password = str(input('--> Установка пароля: ').strip())
        password_two = str(input('--> Установка пароля (повтор): ').strip())

        print(email, username, password, password_two)
        email = Email.objects.create(email = email)

        if not password or not username or not email:
            raise CommandError("Пароли не совпадают")

        if password == password_two:
            user = CustomUser.objects.create(
                username = username,
                is_superuser = True
            )
            user.set_password(password_two)
            user.email.add(email)
            user.save()
            self.stdout.write("Пользователь успешно создан!")
        else:
            raise CommandError("Пароли не совпадают")
            