from django.db import models
from django.utils.translation import gettext_lazy as _


class RefBook(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name=_("Код"))
    name = models.CharField(max_length=300, verbose_name=_("Название"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Справочник")
        verbose_name_plural = _("Справочники")


class RefBookVersion(models.Model):
    refbook = models.ForeignKey(RefBook, related_name="versions", on_delete=models.CASCADE,
                                verbose_name=_("Справочник"))
    version = models.CharField(max_length=50, verbose_name=_("Версия"))
    start_date = models.DateField(verbose_name=_("Дата начала"))

    class Meta:
        unique_together = ('refbook', 'version')
        constraints = [
            models.UniqueConstraint(
                fields=['refbook', 'start_date'],
                name='unique_refbook_start_date'
            )
        ]
        verbose_name = _("Версия справочника")
        verbose_name_plural = _("Версии справочников")

    def __str__(self):
        return f"{self.refbook.name} - {self.version}"


class RefBookElement(models.Model):
    version = models.ForeignKey(RefBookVersion, related_name="elements", on_delete=models.CASCADE, verbose_name=_("Версия"))
    code = models.CharField(max_length=100, verbose_name=_("Код"))
    value = models.CharField(max_length=300, verbose_name=_("Значение"))

    class Meta:
        unique_together = ('version', 'code')
        verbose_name = _("Элемент справочника")
        verbose_name_plural = _("Элементы справочников")

    def __str__(self):
        return f"{self.code}: {self.value}"
