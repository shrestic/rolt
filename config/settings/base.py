# ruff: noqa: ERA001, E501
"""Base settings to build other settings files upon."""

import ssl
from datetime import timedelta
from pathlib import Path

import environ
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# rolt/
APPS_DIR = BASE_DIR / "rolt"
env = environ.Env()

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
USE_TZ = True
TIME_ZONE = "Asia/Ho_Chi_Minh"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#languages
# from django.utils.translation import gettext_lazy as _
# LANGUAGES = [
#     ('en', _('English')),
#     ('fr-fr', _('French')),
#     ('pt-br', _('Portuguese')),
# ]
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "django_celery_beat",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_spectacular",
    "channels",
    "social_django",
]

LOCAL_APPS = [
    # Your stuff: custom apps go here
    "rolt.users",
    "rolt.common",
    "rolt.core",
    "rolt.email",
    "rolt.accounts",
    "rolt.manufacturers",
    "rolt.components",
    "rolt.builds",
    "rolt.accessories",
    "rolt.shop",
    "rolt.chat",
    "rolt.warranty",
    "rolt.inventory",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "rolt.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
# LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
# LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [str(APPS_DIR / "templates")],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Phong Nguyen""", "nhatphongcgp@gmail.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
# https://cookiecutter-django.readthedocs.io/en/latest/settings.html#other-environment-settings

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

REDIS_URL = env("REDIS_URL", default="redis://redis:6379/0")
REDIS_SSL = REDIS_URL.startswith("rediss://")

# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = REDIS_URL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#redis-backend-use-ssl
CELERY_BROKER_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE} if REDIS_SSL else None
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = REDIS_URL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#redis-backend-use-ssl
CELERY_REDIS_BACKEND_USE_SSL = CELERY_BROKER_USE_SSL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
CELERY_RESULT_EXTENDED = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-always-retry
# https://github.com/celery/celery/pull/6122
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-max-retries
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


CELERY_BEAT_SCHEDULE = {
    "update-expired-warranties": {
        "task": "rolt.warranty.tasks.update_expired_warranties",
        "schedule": crontab(hour=0, minute=0),
    },
    "update-order-status": {
        "task": "rolt.shop.tasks.update_order_status",
        "schedule": crontab(minute="*/15"),  # Every 15 minutes
    },
}

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
CELERY_WORKER_SEND_TASK_EVENTS = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_send_sent_event
CELERY_TASK_SEND_SENT_EVENT = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-hijack-root-logger
CELERY_WORKER_HIJACK_ROOT_LOGGER = False

# django-rest-framework
COMPONENTS = [
    "keycap",
    "switch",
    "kit",
    "build",
    "service",
    "showcase",
    "accessory",
    "manufacturer",
    "cart",
    "order",
    "payment",
    "chat",
    "warranty",
    "warranty_request",
]
ACTIONS = {
    "list": env("LIST_RATE", default="100/hour"),
    "detail": env("DETAIL_RATE", default="200/hour"),
    "create": env("CREATE_RATE", default="100/hour"),
    "update": env("UPDATE_RATE", default="100/hour"),
    "delete": env("DELETE_RATE", default="50/hour"),
    "bulk_create": env("BULK_CREATE_RATE", default="20/hour"),
    "room_create": env("ROOM_CREATE_RATE", default="20/hour"),
    "global_list": env("GLOBAL_LIST_RATE", default="1000/hour"),
}

# Create DEFAULT_THROTTLE_RATES dynamic
throttle_rates = {
    "anon": env("ANON_RATE", default="150/hour"),
    "user": env("USER_RATE", default="500/hour"),
}
for component in COMPONENTS:
    for action, rate in ACTIONS.items():
        throttle_rates[f"{component}_{action}"] = rate


REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "rolt.common.exception_handlers.custom_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": throttle_rates,
}

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
CORS_URLS_REGEX = r"^/api/.*$"

# By Default swagger ui is available only to admin user(s). You can change permission classes to change that
# See more configuration options at https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings
SPECTACULAR_SETTINGS = {
    "TITLE": "rolt API",
    "DESCRIPTION": "Documentation of API endpoints of rolt",
    "VERSION": "1.0.0",
    "TAGS": [
        {"name": "auth", "description": "JWT & user auth endpoints"},
        {"name": "users", "description": "User management endpoints"},
        {"name": "schema", "description": "Schema related"},
    ],
    "SWAGGER_UI_SETTINGS": {
        "docExpansion": "none",
    },
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
    "SCHEMA_PATH_PREFIX": "/api/",
}
# Your stuff...
# ------------------------------------------------------------------------------
# SimpleJWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "TOKEN_OBTAIN_SERIALIZER": "rolt.users.serializers.CustomTokenObtainPairSerializer",
}

# Djoser
# ------------------------------------------------------------------------------
# Djoser configuration for user authentication and management
BASE_DJOSER = {
    # Send activation email when user registers
    "SEND_ACTIVATION_EMAIL": True,
    # Send confirmation email when user confirms their email
    "SEND_CONFIRMATION_EMAIL": True,
    # URL pattern for account activation
    "ACTIVATION_URL": "activate/{uid}/{token}",
    # URL pattern for password reset confirmation
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    # Send confirmation email when user changes their password
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    # Require password confirmation when resetting password
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    # Use JWT tokens for social authentication
    "SOCIAL_AUTH_TOKEN_STRATEGY": "djoser.social.token.jwt.TokenStrategy",
    # Custom serializers for different user operations
    "SERIALIZERS": {
        "activation": "djoser.serializers.ActivationSerializer",
        "user_create": "rolt.users.serializers.UserCreateSerializer",
        "user": "rolt.users.serializers.UserSerializer",
        "current_user": "rolt.users.serializers.UserSerializer",
    },
    "EMAIL": {
        "activation": "rolt.email.djoser.CustomActivationEmail",
        "confirmation": "rolt.email.djoser.CustomConfirmationEmail",
        "password_reset": "rolt.email.djoser.CustomPasswordResetEmail",
        "password_changed_confirmation": "rolt.email.djoser.CustomPasswordChangedConfirmationEmail",
    },
}
# Google OAuth
AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

# Google OAuth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env.str("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", "")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env.str("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", "")
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ["email", "profile"]
SOCIAL_AUTH_JSONFIELD_ENABLED = True

# Custom User Model
AUTH_USER_MODEL = "users.BaseUser"

# Email
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")

SUPPORT_ALERT_EMAIL = env("SUPPORT_ALERT_EMAIL")
EMAIL_SENDING_FAILURE_TRIGGER = False

# Channels
ASGI_APPLICATION = "config.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [env("REDIS_URL", default="redis://redis:6379/0")],
        },
    },
}
