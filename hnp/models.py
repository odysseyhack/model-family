from django.db import models

class HNPOAuth(models.Model):
    client_name = models.CharField(max_length=40)
    token = models.CharField(max_length=40, blank=True)

    class Meta:
        verbose_name = "OAuth"
        verbose_name_plural = "OAuth"

    def __str__(self):
        return self.client_name
