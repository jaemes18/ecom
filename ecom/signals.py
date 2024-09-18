
import os
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Product

@receiver(post_save, sender=Product)
def convert_image_format(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if image_path.endswith('.jfif'):
            image = Image.open(image_path)
            new_image_path = image_path.rsplit('.', 1)[0] + '.jpg'
            image.convert('RGB').save(new_image_path, 'JPEG')
            os.remove(image_path)
            instance.image.name = new_image_path.replace(settings.MEDIA_ROOT, '').lstrip('/')
            instance.save()
