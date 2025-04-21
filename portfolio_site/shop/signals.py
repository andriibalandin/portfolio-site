from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category

@receiver(post_migrate)
def create_default_category(sender, **kwargs):
    Category.objects.get_or_create(
        name='Вінілові платівки',
        defaults={
            'slug': 'vinyl-records'
        }
    )