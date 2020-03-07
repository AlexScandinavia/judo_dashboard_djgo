from django.db import models

# Create your models here.


class JudoResult(models.Model):
    """ Model that defines result"""
    result = models.IntegerField()
    event_name = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    date = models.DateTimeField(verbose_name="Competition date")

    class Meta:
        verbose_name = "event result"
        ordering = ['date']

    def __str__(self):
        return self.event_name