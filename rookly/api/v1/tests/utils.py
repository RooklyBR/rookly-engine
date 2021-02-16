from rest_framework.authtoken.models import Token

from rookly.authentication.models import User


def create_user_and_token(nickname="fake"):
    user = User.objects.create_user(
        email="{}@user.com".format(nickname),
        address_cep="00000000",
        address_number=0,
        birth_date="1997-09-08",
    )
    token, create = Token.objects.get_or_create(user=user)
    return (user, token)
