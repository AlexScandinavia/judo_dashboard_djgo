from django.db import models

# Create your models here.

class Judoka(models.Model):
    """ Model that defines result"""
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    birthday = models.DateField(verbose_name="Birthday")
    judoins_id = models.IntegerField()

    class Meta:
        ordering = ['judoins_id']

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

class JudoResult(models.Model):
    """ Model that defines result"""
    result = models.IntegerField()
    event_name = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    date = models.DateField(verbose_name="Competition date")
    judoka = models.ForeignKey('Judoka', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "event result"
        ordering = ['date']

    def __str__(self):
        return self.event_name

