from django.db import models

class Option(models.Model):
    """
    Represents the options for BillReminder's configuration.
    """

    name = models.CharField(
        "Option name", max_length=50
    )

    value = models.CharField(
        "Option value", max_length=150
    )

    def __unicode__(self):
        return "%s: %s" % (self.name, self.valeu)
