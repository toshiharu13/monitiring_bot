from django.db import models


class TypeOfService(models.Model):
    type_of_service = models.CharField('Тип услуги',)
    time_to_work = models.PositiveIntegerField('время работ в днях')
    price = models.IntegerField('Цена услуги')


class Client(models.Model):
    id_telegtam = models.PositiveIntegerField(
        'id клиента',
        unique=True)
    first_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Имя клиента",)
    last_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Фамилия клиента",)
    master = models.BooleanField('является ли клиент мастером')
    customer = models.BooleanField('является ли клиент заказчиком')
    master = models.ForeignKey(TypeOfService,
                               on_delete=models.CASCADE,
                               related_name='Услуги'
                               )

    def __str__(self):
        return f"клиент {self.last_name} {self.last_name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
