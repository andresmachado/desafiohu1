from django.db import models

# Create your models here.


class Hotel(models.Model):
    name = models.CharField('Nome', max_length=255)
    city = models.CharField('Cidade', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hoteis'


class Disponibility(models.Model):
    hotel = models.ForeignKey(Hotel, verbose_name='Hotel', related_name='disponibility')
    date = models.DateField('Data')
    min_nights = models.PositiveSmallIntegerField('Minimo de noites')
    avaiable = models.BooleanField('Disponivel?', default=False)

    def __str__(self):
        return '{}'.format(self.date)

    class Meta:
        ordering = ['date']
        verbose_name = 'Datas'
        verbose_name_plural = 'Datas disponíveis'
