SECRET_KEY = '3u!$=bdo5=55^eudco30#xmvdb&@s%$739%cfas4&t#favoy!5'

DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'graphene_django',
    'django_filters',

    'tests.test_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#ROOT_URLCONF = 'cookbook.urls'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}


GRAPHENE = {
    'SCHEMA': 'schema.schema'
}

