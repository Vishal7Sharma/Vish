from django.db import models


# New blog app

class Blog(models.Model):
    title = models.CharField(max_length=30, blank=True, default='This is the title')
    content = models.CharField(max_length=400, blank=True, default='This is the content')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title
