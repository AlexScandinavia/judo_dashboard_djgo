from django.db import models


# TODO: HEADTOHEAD

class Judoka(models.Model):
    """ Model that defines result"""
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    birthday = models.DateField(verbose_name="Birthday", null=True, blank=True)
    photo = models.ImageField(upload_to="photos_avatar/", default="photos_avatar/avatar-man.jpg", unique=False)
    description = models.CharField(max_length=512)
    judoins_id = models.IntegerField()

    class Meta:
        ordering = ['judoins_id']

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.lower().capitalize()
        self.last_name = self.last_name.upper()
        self.country = self.country.upper()
        super(Judoka, self).save(*args, **kwargs)  # Use the normal save of models.Model

    def return_url(self):
        return "https://www.judoinside.com/judoka/{}".format(self.judoins_id)


class JudoResult(models.Model):
    """ Model that defines a judo result"""
    result = models.IntegerField()
    category = models.CharField(max_length=20)
    date = models.DateField(verbose_name="Competition date")
    judoka = models.ForeignKey('Judoka', on_delete=models.CASCADE)
    event = models.ForeignKey('JudoEvent', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Judo Result"
        ordering = ['date']

    def __str__(self):
        return "{}: {}".format(str(self.result), str(self.event.event_name))


class JudoEvent(models.Model):
    """ Model that defines judo event"""

    event_name = models.CharField(max_length=100)
    event_judoins_id = models.IntegerField()
    date_start = models.DateField(verbose_name="Competition start date")
    date_end = models.DateField(verbose_name="Competition end date")
    event_type = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Judo Event"
        ordering = ['date_start']

    def __str__(self):
        return self.event_name

    def return_url(self):
        return "https://www.judoinside.com/event/{}".format(self.event_judoins_id)
