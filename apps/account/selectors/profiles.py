from apps.account.models import Doctor, Patient


def doctor_profiles():
    return Doctor.objects.select_related('user')


def patient_profiles():
    return Patient.objects.select_related('user')
