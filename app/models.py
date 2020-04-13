from django.db import models


class Judoka(models.Model):
    """ Model that defines result"""

    # General Info
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birthyear = models.IntegerField(verbose_name="Birth year")
    height = models.IntegerField(null=True)
    country = models.CharField(max_length=64)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to="photos_avatar/")
    judobase_id = models.IntegerField(unique=True)

    # Judo characteristics
    fav_tech = models.CharField(max_length=40, null=True)
    category = models.CharField(max_length=100)
    belt = models.CharField(max_length=40, null=True)

    # World Ranking Information
    wrl_points = models.IntegerField(null=True)
    world_ranking = models.IntegerField(null=True)
    wrl_category = models.CharField(max_length=10, null=True)

    class Meta:
        ordering = ['world_ranking']

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.lower().capitalize()
        self.last_name = self.last_name.upper()
        self.country = self.country.upper()
        super(Judoka, self).save(*args, **kwargs)  # Use the normal save of models.Model

    def return_url(self):
        return r"https://judobase.ijf.org/#/competitor/profile/{}".format(self.judobase_id)
