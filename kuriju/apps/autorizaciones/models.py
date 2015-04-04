from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from apps.thumbs import ImageWithThumbsField
# Create your models here.


class perfil(models.Model):
    user=models.OneToOneField(User)
    avatar=ImageWithThumbsField(upload_to='avatar_user/',  null=True, blank=True, verbose_name='avatar', sizes=((125,125),(30,30)))
    class Meta:
        verbose_name = ('perfil')
        verbose_name_plural = ('perfiles')
    def __unicode__(self):
        return '%s' % (self.user.username)

# def create_user_profile(sender, instance, created, **kwargs):
#     """Create the UserProfile when a new User is saved"""
#     if created:
#         userPerfil= perfil()
#         userPerfil.user = instance
#         userPerfil.avatar='default.png'
#         userPerfil.save()

# post_save.connect(create_user_profile, sender=User)


from django.dispatch import receiver
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        perfil.objects.get_or_create(user=instance)

post_save.connect(ensure_profile_exists, sender=User)