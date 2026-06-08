from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from courses.models import User, UserProgress


def token_response_for_user(user):
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'email': user.email,
            'name': f'{user.first_name} {user.last_name}'.strip(),
        },
    })


google_session = requests.Session()
google_session.mount(
    'https://',
    requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=20, max_retries=2),
)
google_request = google_requests.Request(session=google_session)


class GoogleAuthView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = 'auth'

    def post(self, request):
        credential = request.data.get('credential')
        if not credential:
            return Response(
                {'error': 'No credential provided'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            idinfo = id_token.verify_oauth2_token(
                credential,
                google_request,
                settings.GOOGLE_CLIENT_ID,
            )
        except ValueError:
            return Response(
                {'error': 'Invalid or expired token'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        email = idinfo.get('email')
        if not email or not idinfo.get('email_verified'):
            return Response(
                {'error': 'Google account email must be verified'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        name = idinfo.get('name', '')
        parts = name.split(' ', 1)

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'first_name': parts[0],
                'last_name': parts[1] if len(parts) > 1 else '',
            },
        )

        if created:
            UserProgress.objects.create(user=user)

        return token_response_for_user(user)
