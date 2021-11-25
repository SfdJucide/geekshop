import requests
from django.utils.datetime_safe import datetime
from social_core.exceptions import AuthForbidden

from users.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    url_method = 'https://api.vk.com/method/'
    access_token = response.get('access_token')
    fields = ','.join(['bdate', 'sex', 'about'])

    api_url = f'{url_method}users.get?fields={fields}&access_token={access_token}&v=5.131'

    response = requests.get(api_url)
    if response.status_code != 200:
        return

    data_json = response.json()['response'][0]

    if 'sex' in data_json:
        if data_json['sex'] == 1:
            user.userprofile.gender = UserProfile.FEMALE
        elif data_json['sex'] == 2:
            user.userprofile.gender = UserProfile.MALE

    if 'bdate' in data_json:
        birth = datetime.strftime(data_json['bdate'], '%d.%m.%Y')

        age = datetime.now().year - birth.year
        if age < 100:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    if 'about' in data_json:
        user.userprofile.about_me = data_json['about']

    user.save()

