from django.contrib.auth import get_user_model
from django.db import models

from django.dispatch import receiver
from django.core.validators import MinValueValidator
from django.db.models.signals import pre_save

import requests
from environs import Env


User = get_user_model()

env = Env()
env.read_env()


class Salon(models.Model):
    name = models.CharField(verbose_name='Название салона', max_length=200, db_index=True)
    address = models.TextField(verbose_name='Адрес', max_length=200, db_index=True, blank=True)

    class Meta:
        verbose_name = 'салон'
        verbose_name_plural = 'салоны'

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField('Название процедуры', max_length=200, db_index=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2,
                                 validators=[MinValueValidator(0)])
    salon_service = models.ManyToManyField('Salon', verbose_name='Услуги салона',
                                           related_name='salon_services', blank=True)
    # master_service = models.ManyToManyField('Master', verbose_name='Услуги салона',
    #                                         related_name='master_services', blank=True)

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'услуги'

    def __str__(self):
        return self.name


class Master(models.Model):
    firstname = models.CharField('Имя', max_length=200, db_index=True)
    lastname = models.CharField('Фамилия', max_length=200, db_index=True)
    foto = models.ImageField(verbose_name='Фото', upload_to='foto', blank=True)
    master_service = models.ManyToManyField('Service', verbose_name='Услуги', related_name='master_services', blank=True)
    master_salon = models.ManyToManyField('Salon', verbose_name='Салон', related_name='master_salons', blank=True)

    class Meta:
        verbose_name = 'мастер'
        verbose_name_plural = 'мастера'

    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class Time(models.Model):
    time = models.DateTimeField(verbose_name='Время')
    available = models.BooleanField(verbose_name='Доступно', default=True)
    master = models.ManyToManyField('Master', verbose_name='Мастер', related_name='available_time', blank=True)
    salon = models.ManyToManyField('Salon', verbose_name='Салон', related_name='available_time', blank=True)

    class Meta:
        verbose_name = 'время'
        verbose_name_plural = 'время'

    def __str__(self):
        return str(f'{self.time.hour} : {self.time.minute}{self.time.minute}')

class Feedback(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='complaints', on_delete=models.CASCADE)
    master = models.ForeignKey('Master', related_name='feedbacks', on_delete=models.CASCADE)
    feedback = models.TextField(verbose_name='Feedback')

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return str(self.user)

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='orders', on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, verbose_name='Салон', related_name='orders', on_delete=models.CASCADE, blank=True)
    master = models.ForeignKey(Master, verbose_name='Мастер', related_name='orders', on_delete=models.CASCADE, blank=True)
    service = models.ForeignKey(Service, verbose_name='Услуга', related_name='orders', on_delete=models.CASCADE, blank=True)
    time = models.ForeignKey(Time, verbose_name='Время', related_name='orders', on_delete=models.CASCADE, blank=True)
    paid = models.BooleanField(verbose_name='Оплачено', default=False)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return str(self.user)


class Advertising(models.Model):
    url = models.URLField('Ссылка', blank=True)
    text = models.TextField('Текст рекламы')
    responses = models.IntegerField(
        'Количество откликов',
        null=True,
        blank=True,
        default=0,
    )

    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Реклама'


@receiver(pre_save, sender=Advertising)
def pre_save_advertising(sender, instance, **kwargs):
    if not instance.pk:
        url = "https://t.ly/api/v1/link/shorten"
        headers = {
            "Authorization": f"Bearer {env.str('TLY_API_TOKEN')}"
        }
        payload = {
            "long_url": "https://firmbarbershop.ru/"
        }
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        instance.url = response.json()["short_url"]
        instance.responses = 0
