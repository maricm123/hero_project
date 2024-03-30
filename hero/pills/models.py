from django.db import models


class PillManager(models.Manager):
    def get_device_configs(self, device_config):
        return self.select_related("device_config").filter(device_config=device_config)


class Pill(models.Model):
    slot = models.CharField(max_length=512)
    name = models.CharField(max_length=512)
    dosage = models.CharField(max_length=512)
    expires = models.DateField()
    passcode_required = models.BooleanField(default=True)
    form = models.CharField(max_length=512)
    exact_pill_count = models.IntegerField(null=True)
    max_manual_doses = models.IntegerField(null=True)

    device_config = models.ForeignKey(
        "config.Config",
        related_name='pills',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    objects = PillManager()

    @classmethod
    def create(cls, pills, config):
        created_pills = []
        for pill_attributes in pills:
            pill = cls.objects.create(**pill_attributes, device_config=config)
            created_pills.append(pill)

        return created_pills
