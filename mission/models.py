from django.db import models


class Target(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-complete", "name"]


class Mission(models.Model):
    targets = models.ManyToManyField("mission.Target", related_name="missions")
    spy_cat = models.ForeignKey(
        "cat.SpyCat", on_delete=models.SET_NULL, null=True, blank=True
    )
    complete = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.targets.all().delete()
        super().delete(*args, **kwargs)
