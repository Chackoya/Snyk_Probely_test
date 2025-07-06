from django.db import models


class Finding(models.Model):

    # base fields
    id = models.IntegerField(primary_key=True)  # Comes from API as int
    target_id = models.CharField(max_length=64)
    definition_id = models.CharField(max_length=64)

    scans = models.JSONField()  # api comes as a list of str

    url = models.URLField(max_length=512)
    path = models.TextField()  # some urls paths can be very large...
    #! NOTE in sqlite Charfields & Textfields etc all become TEXT...

    method = models.CharField(max_length=16)

    # some extras
    severity = models.IntegerField(null=True, blank=True)
    fix = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=32, null=True, blank=True)
    evidence = models.TextField(null=True, blank=True)
    last_found = models.DateTimeField(null=True, blank=True)
