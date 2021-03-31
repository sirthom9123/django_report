from django.db import models
from django.urls import reverse
from profiles.models import Profile


class Report(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='reports', blank=True)
    remarks = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created',)
    
    def get_absolute_url(self):
        return reverse("reports:report_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.name
    
    
    