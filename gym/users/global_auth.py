from jose import jwt, JWTError
from ninja.security import HttpBearer
from django.conf import settings
from datetime import datetime, timedelta

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            user_pk = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        except JWTError as e:
            print(str(e))
            return {
                'token': 'unauthorized',
            }
        
        if user_pk:
            return {
                'pk': str(user_pk['pk'])
            }

def get_user_token(user):
    
    expiration_time = datetime.utcnow() + timedelta(minutes=1)
    
    token = jwt.encode(
        {
            'pk': str(user.pk),
            'exp': expiration_time.timestamp()
        },
        key=settings.SECRET_KEY,
        algorithm='HS256'
    )
    return {
        'access': str(token),
    }
    
def get_user_refresh_token(user):
    
    expiration_time = datetime.utcnow() + timedelta(days=4)
    
    token = jwt.encode(
        {
            'pk': str(user.pk),
            'exp': expiration_time.timestamp()
        },
        key=settings.SECRET_KEY,
        algorithm='HS256'
    )
    return {
        'refresh': str(token),
    }