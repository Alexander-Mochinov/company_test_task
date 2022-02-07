from collections import defaultdict
import re
from typing import Any
from xml.dom.minidom import Childless
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.forms import model_to_dict
from django.core.validators import RegexValidator
import json
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomErrors(Exception):
    """
    Кастомный класс (Хотел выставить лимит на вложенность с помощью этого класса)
    """
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message



class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Модель сущьности пользователя (Решил переопределить пользователя, для более гибкой логики)
    """

    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('-', 'Не определен'),
    )
    username = models.CharField(
        verbose_name = 'Пользователь',
        max_length=64,
        unique=True
    )

    first_name = models.CharField(
        verbose_name = 'Имя',
        max_length=25,
        unique=True
    )

    second_name = models.CharField(
        verbose_name = 'Фамилия',
        max_length=25,
        unique=True
    )

    patronymic = models.CharField(
        verbose_name = 'Отчество',
        max_length=25,
        unique=True
    )
    gender = models.CharField(
        max_length=24, 
        verbose_name="Пол", 
        choices=GENDER_CHOICES, 
        default="-", 
        blank=True
    )
    email = models.ManyToManyField(
        'Email', 
        verbose_name='Почта',
        default=None,
        related_name='email_users',
    )

    date_joined = models.DateTimeField(
        verbose_name = 'Дата создании', 
        auto_now_add=True,
    )
    date_of_change = models.DateTimeField(
        verbose_name = 'Дата изменения', 
        auto_now_add=True,
    )
    date_status_change = models.DateTimeField(
        verbose_name = 'Дата изменения статуса', 
        auto_now_add=True,
    )
    is_active = models.BooleanField(
        verbose_name = 'is_active', 
        default=True
    )

    is_admin = models.BooleanField(
        verbose_name = 'is_admin', 
        default=True
    )
    is_staff = models.BooleanField(
        verbose_name = 'is_staff',
        default=False
    )
    timezone = models.CharField(
        max_length=64, 
        verbose_name="Часовой пояс",
        default="MSC", 
        blank=True
    )
 
    objects = UserManager()
 
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
 
    def __str__(self) -> str:
        return str(self.username)

    def get_gender(self) -> str:
        """
        Получение гендарной пренадлежности
        """
        return str(dict(CustomUser.GENDER_CHOICES)[self.gender])

    def to_json(self) -> json:
        return model_to_dict(self)
        
    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Client(models.Model):
    """
    Модель сущности клиента
    """

    TYPE_CHOICES = (
        ('primary', 'Первичный'),
        ('secondary', 'Повторный'),
        ('external', 'Внешний'),
        ('indirect', 'Косвенный'),
    )

    personal_id = models.PositiveIntegerField(
        verbose_name = 'Идентификационный номер клиента',
        null=True,
        unique=True
    )
    phone_regex = RegexValidator(regex=r'^\+7\d{10}$')

    user = models.OneToOneField(
        CustomUser,
        verbose_name = 'Пользователь',
        related_name = 'client_user',
        on_delete = models.CASCADE,
    )
    type = models.CharField(
        max_length=24, 
        verbose_name="Тип", 
        choices=TYPE_CHOICES, 
        default="primary", 
        blank=True
    )

    phone_number = models.CharField(
        'Номер телефона пациента', 
        blank=True, 
        validators=[phone_regex], 
        max_length=12,
        unique=True
    )

    social_network = models.ManyToManyField(
        'SocialNetworks', 
        verbose_name='Социальные сети', 
        through='SocialNetworksRef'
    )

    departments = models.ManyToManyField(
        'Department', 
        verbose_name='Департаменты', 
        through='DepartmentClientRef'
    )

    def get_type(self) -> str:
        """
        Получение типа клиента
        """
        return str(dict(Client.TYPE_CHOICES)[self.type])

    def __str__(self) -> str:
        return f'{self.user.username} : {self.personal_id}'

    def to_json(self) -> json:
        return model_to_dict(self)

    class Meta:
        db_table = 'client'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Email(models.Model):
    """
    Сущность для хранения поля
    """
    email = models.EmailField(
        verbose_name = 'Email',
        default=None,
        null=True,
    )

    def __str__(self) -> str:
        if self.email:
            return self.email
        return ''

    class Meta:
        db_table = 'email'
        verbose_name = 'Почта'
        verbose_name_plural = 'Почты'


class LegalEntity(models.Model):
    """
    Модель сущности  Юр. лица
    """

    personal_id = models.PositiveIntegerField(
        verbose_name = 'Идентификационный номер Юр. лица',
        null=True,
        unique=True
    )
    date_joined = models.DateTimeField(
        verbose_name = 'Дата создании', 
        auto_now_add=True,
    )
    date_of_change = models.DateTimeField(
        verbose_name = 'Дата изменения', 
        auto_now_add=True,
    )
    date_status_change = models.DateTimeField(
        verbose_name = 'Дата изменения статуса', 
        auto_now_add=True,
    )

    full_name = models.CharField(
        max_length=128, 
        verbose_name="Полное наименование организации",
        blank=True
    )

    short_name = models.CharField(
        max_length=128, 
        verbose_name="Сокращённое наименование организации",
        blank=True
    )
 
    INN = models.CharField(
        verbose_name = 'Идентификационный номер налогоплательщика',
        max_length = 12,
        null = False,
        unique = True
    )

    KPP = models.CharField(
        verbose_name = 'Код причины постановки на учёт',
        max_length = 12,
        null = False,
        unique = True
    )
    departments = models.ManyToManyField('Department', verbose_name='Департаменты', through='DepartmentLegalEntityRef')


    @property
    def get_kpp(self) -> str:
        """
        Вывод KPP Юр. лица
        """
        return self.INN

    @property
    def get_inn(self) -> str:
        """
        Вывод INN  Юр. лица
        """
        return self.INN
    
    def get_count_departament(self) -> int:
        """
        Получение кол-во департаментов в организации
        """
        return self.entity_departament.all().count()
 
    def __str__(self) -> str:
        return f'{self.full_name} : {self.personal_id}'

    def to_json(self) -> json:
        return model_to_dict(self)

    class Meta:
        db_table = 'legal_entity'
        verbose_name = 'Юр. лицо'
        verbose_name_plural = 'Юр. лица'

class Department(models.Model):
    """
    Сущность Департамента
    """
    personal_id = models.PositiveIntegerField(
        verbose_name = 'Идентификационный номер департамента',
        null=True,
        unique=True
    )

    name = models.CharField(
        max_length=128, 
        verbose_name="Наименование департамента",
        blank=True
    )
    parent = models.ForeignKey(
		'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='parent_dep', verbose_name='Родительский департамент'
	)

    def get_count_clients(self) -> int:
        """
        Получение кол-во клиентов в департаменте
        """
        return self.client_departament.all().count()

    def has_children(self) -> bool:
        """
        Проверка есть ли id в списке дочерних
        """
        return self.id in [_.id for _ in self.get_children(self.parent_dep.all())]

    def get_children(self, items) -> list:
        """
        Получение дочерних записей
        """
        department_list = []
        if items:
            for item in items:
                department_list.append(item)
                department_list.extend(self.get_children(item.parent_dep.all()))
        return department_list
        

    def get_parent_entity(self) -> bool:
        """
        Получение родительских записей
        """
        PARENT_LIST = []
        department = Department.objects.get(id = self.id)
        while department.parent:
            department = department.parent
            PARENT_LIST.append(department)

        if len(PARENT_LIST) < 6:
            return True
        return False

    def save(self, *args, **kwargs):
        """
        Переопределяем метод для проверки на вложенность
        Устанавливаем personal_id получаем последний 
        """
        if self.parent:
            if self.get_parent_entity() and (self.get_children() == False):
                super(Department, self).save(*args, **kwargs)
        else:
            super(Department, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f'{self.name} : {self.personal_id}'

    def to_json(self) -> json:
        return model_to_dict(self)

    class Meta:
        db_table = 'department'
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'


class DepartmentLegalEntityRef(models.Model):
    """
    M2M Модель для промежуточной сущности Department и LegalEntity
    """
    department = models.ForeignKey(
		Department, on_delete=models.CASCADE, null=True,   blank=True, verbose_name='департамент'
	)

    legal_entity = models.ForeignKey(
		LegalEntity, on_delete=models.CASCADE, null=True,related_name='entity_departament', blank=True, verbose_name='Юр. лицо'
	)

    def save(self, *args, **kwargs):
        """
        Переопределяем метод для дополнительной логики на проверку существующей связи
        """
        note = DepartmentLegalEntityRef.objects.filter(
            legal_entity = self.legal_entity,
            department = self.department
        )
        if not note.exists():
            super(DepartmentLegalEntityRef, self).save(*args, **kwargs)

    def to_json(self) -> json:
        return model_to_dict(self)

class DepartmentClientRef(models.Model):
    """
    M2M Модель для промежуточной сущности Department и Client
    """
    department = models.ForeignKey(
		Department, on_delete=models.CASCADE, null=True, related_name='client_departament', blank=True, verbose_name='Департамент'
	)
    client = models.ForeignKey(
		Client, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Физ лицо'
	)
    date_joined = models.DateTimeField(
        verbose_name = 'Дата присоединения', 
        auto_now_add=True,
        blank=False,
    )

    def save(self, *args, **kwargs):
        """
        Переопределяем метод для дополнительной логики на проверку существующей связи
        """
        note = DepartmentClientRef.objects.filter(
            department = self.department,
            client = self.client
        )
        if not note.exists():
            super(DepartmentClientRef, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.id}: {self.client.user.username}'

    def to_json(self) -> json:
        return model_to_dict(self)

class SocialNetworksRef(models.Model):
    """
    M2M Модель для промежуточной сущности Client и SocialNetworks
    """
    client = models.ForeignKey(
		Client, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Клиент'
	)

    social_networks = models.ForeignKey(
		'SocialNetworks', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Соц. сеть'
	)

    url = models.CharField(
        max_length=999, 
        verbose_name="Адрес сети", 
        blank=False
    )

    def save(self, *args, **kwargs):
        """
        Переопределяем метод для дополнительной логики на проверку существующей связи
        """
        note = SocialNetworksRef.objects.filter(
            social_networks = self.social_networks,
            client = self.client
        )
        if self.social_networks.count_extend > note.count():
            super(SocialNetworks, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.client.user.username} : {self.social_networks.get_name}'

    def to_json(self) -> json:
        return model_to_dict(self)

class SocialNetworks(models.Model):
    """
    Социальные сети
    """

    SOCIAL_CONTACT = (
        ('VK', 'VK'),
        ('FB','Facebook'),
        ('ОК','Оk'),
        ('INST','Instagram'),
        ('TEG','Telegram'),
        ('WA','WhatsApp'),
        ('VB', 'Viber'),
    )
    name = models.CharField(
        max_length=24, 
        verbose_name="Социальная сеть", 
        choices=SOCIAL_CONTACT,
        default="",
        unique=True,
        blank=False
    )
    count_extend = models.PositiveSmallIntegerField(
        verbose_name='Кол-во использований пользователем',
        default=1
    )

    def get_name(self) -> str:
        """
        Получение имя соц. сети
        """
        return str(dict(SocialNetworks.SOCIAL_CONTACT)[self.name])

    def __str__(self) -> str:
        return self.get_name()

    def to_json(self) -> json:
        return model_to_dict(self)

    class Meta:
        db_table = 'social_networks'
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'


@receiver(post_save, sender=Client)
def create_or_update_client(sender, instance, created, **kwargs):
    if created:
        if instance.id:
            instance.personal_id = int(f'{instance.id}01')
            instance.save()

@receiver(post_save, sender=LegalEntity)
def create_or_update_legal_entity(sender, instance, created, **kwargs):
    if created:
        if instance.id:
            instance.personal_id = int(f'{instance.id}02')
            instance.save()

@receiver(post_save, sender=Department)
def create_or_update_department(sender, instance, created, **kwargs):
    if created:
        if instance.id:
            instance.personal_id = int(f'{instance.id}03')
            instance.save()