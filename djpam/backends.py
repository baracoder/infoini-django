# coding=utf-8
# dem beispiel nach
# http://blogs.translucentcode.org/mick/2006/06/09/djangos-new-authentication-backends/
# und http://atlee.ca/software/pam/
# siehe auch dokumentation
# https://docs.djangoproject.com/en/1.2/topics/auth/#other-authentication-sources

# installation:
# AUTHENTICATION_BACKENDS in der settings.py datei erweitern um:
# 'djpam.backends.PAMBackend',



import pam
from django.contrib.auth.models import User

class PAMBackend:
    def authenticate(self, username=None,password=None):
        if pam.authenticate(username,password):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)

                # Standard: Kein Zugriff zum Admin-Interface, kein
                # Superuser
                user.is_staff = False
                user.is_superuser = False

                # wichtig! da das Passwort nicht benutzt wird
                # wir können aber kein standardpasswort setzen, da sonst
                # alle mit dem standardpasswort einloggen können!
                user.set_unusable_password()
                user.save()
            return user
        return None

    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
