from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
        
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        # Set the name field value based on the slug field value with first letter of each word capitalized
        words = self.slug.split('-')
        self.name = ' '.join([word.capitalize() for word in words])
        super(Tag, self).save(*args, **kwargs)
