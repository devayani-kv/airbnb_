from django.db import models

# Create your models here.
class inputs(models.Model):
    link = models.CharField(max_length = 1000)

    def __self__(self):
        return self.link