from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import Doctor, Patient


class AppointmentDay(models.Model):
    day = models.DateField(_('تاریخ'))

    def __str__(self):
        return self.day.strftime('%Y-%m-%d')
    
    class Meta:
        verbose_name = _('تاریخ نوبت')
        verbose_name_plural = _('تاریخچه نوبت ها')
        ordering = ('-day',)


class AvailableTime(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='available_times', verbose_name=_('پزشک'))
    date = models.ForeignKey(AppointmentDay, on_delete=models.CASCADE, related_name="available_dates", verbose_name=_('تاریخ'))
    start_time = models.TimeField(_('زمان شروع'))
    end_time = models.TimeField(_('زمان پایان'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال'))

    def __str__(self):
        return f"{self.doctor} - {self.date.day} ({self.start_time} - {self.end_time})"

    class Meta:
        verbose_name = _('زمان در دسترس')
        verbose_name_plural = _('زمان‌های در دسترس')
        ordering = ('-date', '-start_time',)


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments', verbose_name=_('پزشک'))
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', verbose_name=_('بیمار'))
    date = models.ForeignKey(AppointmentDay, on_delete=models.CASCADE, related_name="reserve_date", verbose_name=_('تاریخ'))
    time = models.TimeField(_('ساعت'))
    is_confirmed = models.BooleanField(default=False, verbose_name=_('ثبت شده'))

    def __str__(self):
        return f"{self.patient.user.full_name} - {self.doctor.user.full_name} at {self.date.day} {self.time}"

    class Meta:
        verbose_name = _('نوبت')
        verbose_name_plural = _('نوبت ها')
        ordering = ('-date', '-time',)
