from django.db import models
#! This model is used for creating generic relationships so I don't need to import the product class from the store directory
from django.contrib.contenttypes.models import ContentType
#! Used to create Generic relationship
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Tag(models.Model):
  label = models.CharField(max_length=250)

#! This tag is used to determine what tag is applied to which object
class TaggedItem(models.Model):
  tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey()
