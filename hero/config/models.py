from django.db import models, transaction
from django.core.exceptions import ValidationError


class ConfigManager(models.Manager):
    def last_active(self, device_id):
        return self.filter(device_id=device_id).last()

    def get_active_config(self, device_id):
        return self.get(device_id=device_id, is_active=True)


class Config(models.Model):
    device_id = models.IntegerField()
    passcode = models.CharField(max_length=4)
    timezone_name = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    objects = ConfigManager()

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs):
        device_id = kwargs.get("device_id")
        try:
            old_config = Config.objects.last_active(device_id)
            if old_config:
                old_config.deactivate()
        except Config.DoesNotExist:
            pass
        except Exception as e:
            raise ValidationError(e)
        try:
            new_config = cls.objects.create(
                **kwargs
            )
        except Exception as e:
            raise ValidationError(e)
        return new_config

    def deactivate(self):
        self.is_active = False
        self.save()
