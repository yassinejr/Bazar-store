from datetime import date, datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    country = CountryField()
    birth = models.DateField(auto_now_add=False, auto_now=False, default=date.today)
    image = models.ImageField(upload_to='images/profile_img/', null=True, blank=True, verbose_name=_('Image'))
    join_date = models.DateTimeField(default=datetime.now, null=True, blank=True, verbose_name=_('Joined at'))
    slug = models.SlugField(blank=True, null=True, verbose_name='Slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user)
        super(Profile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return str(self.user)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user = User.objects.get(username=kwargs['instance'])
        user_name = user.first_name + " " + user.last_name
        user_email = user.email
        user_profile = Profile.objects.create(user=kwargs['instance'], name=user_name, email=user_email)


post_save.connect(create_profile, sender=User)
