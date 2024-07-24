from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# from phonenumber_field.modelfields import PhoneNumberField


class Salon(models.Model):
    name = models.CharField('ФИО владельца', max_length=200, db_index=True)
    address = models.TextField('Адрес')


class Master(models.Model):
    firstname = models.CharField('Имя', max_length=200, db_index=True)
    lastname = models.CharField('Фамилия', max_length=200, db_index=True)
    speciality = models.CharField('Специальность', max_length=200, db_index=True)
    foto = models.ImageField(blank=True)
    salon = models.ManyToManyField('Salon', related_name='masters', blank=True)


# class Procedure(models.Model):
#     name = models.CharField('ФИО владельца', max_length=200, db_index=True)
#     price = models.DecimalField()
#     master = models.ManyToManyField('Master', related_name='procedures')


# class Feedback(models.Model):
#     user = models.ForeignKey(User, verbose_name='Пользователь', related_name='complaints', on_delete=models.CASCADE)
#     master = models.ForeignKey('Master', related_name='feedbacks' ,on_delete=models.CASCADE)
#     feedback = models.TextField('Feedback')


# class Order(models.Model):
#     user = models.ForeignKey(User, verbose_name='Пользователь', related_name='complaints', on_delete=models.CASCADE)
#     salon = models.ForeignKey('Salon', related_name='orders' ,on_delete=models.CASCADE)
#     master = models.ForeignKey('Master', related_name='orders' ,on_delete=models.CASCADE)
#     procedure = models.ForeignKey('Procedure', related_name='orders' ,on_delete=models.CASCADE)
#     paid = models.BooleanField()


# class OrderElements(models.Model):


