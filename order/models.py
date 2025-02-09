from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from core.models import CreateMixin, UpdateMixin


class AppointmentOrder(CreateMixin, UpdateMixin):
    TRACKING_CODE_LENGTH = 10 

    STATUS_CHOICES = (
        ('pending', _('در انتظار تایید')),
        ('confirmed', _('تایید شده')),
        ('cancelled', _('لغو شده')),
        ('completed', _('انجام شده')),
    )

    patient = models.ForeignKey('account.Patient', on_delete=models.CASCADE, related_name='orders', verbose_name=_('بیمار'))
    doctor = models.ForeignKey('account.Doctor', on_delete=models.CASCADE, related_name='orders', verbose_name=_('پزشک'))
    appointment = models.OneToOneField('appointment.Appointment', on_delete=models.CASCADE, related_name='order', verbose_name=_('نوبت'))
    
    tracking_code = models.CharField(max_length=TRACKING_CODE_LENGTH, unique=True, editable=False, verbose_name=_('کد رهگیری'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name=_('وضعیت'))


    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = str(uuid.uuid4().int)[:self.TRACKING_CODE_LENGTH]
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Order {self.tracking_code} - {self.patient.user.get_full_name()} - {self.appointment.date}"


    class Meta:
        verbose_name = _('سفارش نوبت')
        verbose_name_plural = _('سفارش‌های نوبت')
        ordering = ('-create_at',)



class Invoice(CreateMixin):
    order = models.OneToOneField(AppointmentOrder, on_delete=models.CASCADE, related_name='invoice', verbose_name=_('نوبت'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('مبلغ ویزیت'))
    description = models.TextField(null=True, blank=True, verbose_name=_('توضیحات'))


    def __str__(self):
        return f"فاکتور برای {self.order.tracking_code} - {self.amount} تومان"

    class Meta:
        verbose_name = _('فاکتور')
        verbose_name_plural = _('فاکتورها')
        ordering = ('-create_at',)
