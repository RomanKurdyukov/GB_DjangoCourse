import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'google-oauth2':
        return
    else:
        url = "https://people.googleapis.com/v1/people/me?personFields=genders,birthdays"
        headers = {
            "Authorization": "Bearer " + response['access_token']
        }
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            return
        data = resp.json()
        if data['birthdays'][1]['date']['year']:
            user_year = data['birthdays'][1]['date']['year']
            age = timezone.now().date().year - user_year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.google.GoogleOAuth2')
            else:
                user.age = age
                user.shopuserprofile.about_me = data['birthdays'][1]['date']
        if data['genders'][0]['value']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['genders'][0]['value'] == 'male' \
                else ShopUserProfile.FEMALE
        user.save()



