from rest_framework import permissions, generics
from rest_framework.response import Response


class UserRoleAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if hasattr(user, 'doctor_profile'):
            return Response({
                "role": "doctor",
                "related_id": user.doctor_profile.id
            })
        elif hasattr(user, 'patient_user'):
            return Response({
                "role": "patient",
                "related_id": user.patient_user.id
            })
        else:
            return Response({
                "role": "unknown",
                "related_id": None
            })
