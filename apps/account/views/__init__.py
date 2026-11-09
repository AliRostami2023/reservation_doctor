"""API views, grouped by domain/use case."""
from .auth_views import CreatePatientAPIView, VerifyCodeAPIView, ResendOtpCodeAPIView, PasswordResetAPIView, ConfirmResetPasswordAPIView
from .doctor_views import CreateDoctorAPIView, ListDoctorProfileAPIView, RetriveDoctorProfileAPIView, UpdateDoctorProfileAPIView
from .patient_views import ListPatientProfileAPIView, RetrivePatientProfileAPIView, UpdatePatientProfileAPIView
from .user_views import UserRoleAPIView

__all__ = ['CreatePatientAPIView', 'VerifyCodeAPIView', 'ResendOtpCodeAPIView', 'PasswordResetAPIView', 'ConfirmResetPasswordAPIView', 'CreateDoctorAPIView', 'ListDoctorProfileAPIView', 'RetriveDoctorProfileAPIView', 'UpdateDoctorProfileAPIView', 'ListPatientProfileAPIView', 'RetrivePatientProfileAPIView', 'UpdatePatientProfileAPIView', 'UserRoleAPIView']
