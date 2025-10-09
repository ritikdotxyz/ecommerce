from django.utils.text import slugify
import uuid

def generate_slug(text, model):
    slug = slugify(text)

    while (model.objects.filter(slug=slug).exists()):
        slug = f"{slugify(text)}-{str(uuid.uuid4())[:4]}"

    return slug