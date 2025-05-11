from django.db import models

class Proteins(models.Model):
    name = models.CharField(max_length=255, unique=True)
    sequence = models.TextField()
    source = models.CharField(max_length=255, blank=True, null=True)  # Example: "NCBI", "UniProt"
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
