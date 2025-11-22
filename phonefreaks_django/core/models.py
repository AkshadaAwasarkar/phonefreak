from django.db import models
from django.contrib.auth.models import User

class Phone(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField()
    tags = models.JSONField(default=list)
    specs = models.JSONField(default=dict)
    prices = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.brand} {self.model}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.phone.model}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'phone')

class Comparison(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone1 = models.ForeignKey(Phone, on_delete=models.CASCADE, related_name='comparisons_as_phone1')
    phone2 = models.ForeignKey(Phone, on_delete=models.CASCADE, related_name='comparisons_as_phone2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.phone1.model} vs {self.phone2.model}"

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
