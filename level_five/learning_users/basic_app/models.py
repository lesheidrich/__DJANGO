from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional classes
    portfolio_site = models.URLField(blank=True)
    # save people's images in ./basic_app/media/profile_pics/
    # DON't FOGET TO INSTALL PILLOW
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self) -> str:
        return self.user.username
