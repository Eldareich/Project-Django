from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import UserProfile, Account
from django.shortcuts import get_object_or_404


@receiver(post_save, sender=Account)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            userprofile=instance,
        )
    else:
        profile = get_object_or_404(UserProfile, userprofile=instance)
        profile.save()


@receiver(post_save, sender=UserProfile)
def update_user(sender, instance, created, **kwargs):
    profile = instance
    if created == False:
        user = get_object_or_404(Account, id=profile.userprofile.id)
        if user.email != profile.userprofile.email:
            user.email = profile.userprofile.email
            user.save()
