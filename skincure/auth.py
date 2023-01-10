from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import authentication_classes


class SessionCsrfExemptAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass

def ignore_csrf(view_func):
    return authentication_classes([SessionCsrfExemptAuthentication])(view_func)