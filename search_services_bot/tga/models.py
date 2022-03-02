from django.db import models


class TypeOfService(models.Model):
    type_of_service = models.CharField(
        'Тип услуги',
        max_length=100,)

    def __str__(self):
        return self.type_of_service

    class Meta:
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Тип услуги'


class Service(models.Model):
    type_of_service = models.ForeignKey(TypeOfService,
                                        verbose_name='Тип услуги',
                                        on_delete=models.PROTECT,
                                        )
    time_to_work = models.PositiveIntegerField('время работ в днях')
    price = models.IntegerField('Цена услуги')

    def __str__(self):
        return self.type_of_service__type_of_service

    class Meta:
        verbose_name = 'Предоставляемая услуга'
        verbose_name_plural = 'Предоставляемые услуги'


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
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='Услуги',
        null=True,
        blank=True,
        verbose_name="Имя клиента",
    )

    def __str__(self):
        return f"клиент {self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
