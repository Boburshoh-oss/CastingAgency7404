from functools import wraps
from urllib.request import urlopen
from flask import request
import json
from jose import jwt


AUTH0_DOMAIN = 'capstone-7404.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone-api'


class AuthError(Exception):
    """A standardized way to communicate auth failures"""
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """
    Obtains the access token from the authorization header
    :return: token
    """
    token = request.headers.get('Authorization')

    if not token:
        raise AuthError('no authorization header', 401)

    # analyse token parts
    token_parts = token.split()

    # should have 2 parts
    if len(token_parts) != 2:
        raise AuthError('authorization token should contain two parts', 401)

    bearer = token_parts[0]
    token = token_parts[1]

    # first part should be 'Bearer'
    if bearer.capitalize() != 'Bearer':
        raise AuthError('first part of the token should be Bearer', 401)

    return token


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


def check_permissions(permission, payload):
    permissions = payload.get('permissions')
    if not permissions or permission not in permissions:
        raise AuthError('unauthorized', 403)
    return True


def requires_auth(permission=''):
    """
    ensures user is authenticated and authorized to access the endpoint
    :param permission: the permissions required to access the endpoint
    """
    def requires_auth_decorator(f):
        """
        auth decorator to reuse in protecting endpoints
        :param f: endpoint that we'll be protecting
        """
        @wraps(f)
        def wrapper(*args, **kwargs):
            """
            ensures request has Authorization header with bearer token
            verifies the given token and checks the permissions embedded within it
            appropriate exceptions are raised if any step fails, else, access is granted
            """
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator