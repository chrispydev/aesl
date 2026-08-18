from pathlib import Path
from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

CONN_MAX_AGE = 60

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "162.0.211.66",
    "aesl.com.gh",
    "www.aesl.com.gh"
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Your apps
    "frontend",
    # Third-party
    "django_browser_reload",
    "rest_framework",
    'django_ckeditor_5',
    # "ckeditor",
    # "ckeditor_uploader",
    "django_cleanup.apps.CleanupConfig",
]

# ==========================
# CKEDITOR SETTINGS
# ==========================

CKEDITOR_UPLOAD_PATH = "content/ckeditor/"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 400,
        "width": "100%",
    },
}

# Only add this in development to avoid serving static in runserver when
# DEBUG=True
if DEBUG:
    INSTALLED_APPS.insert(0, "whitenoise.runserver_nostatic")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Must be near the top
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "aesl.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Custom
                "frontend.context_processors.people_navigation",
            ],
        },
    },
]

WSGI_APPLICATION = "aesl.wsgi.application"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# Database (SQLite is fine for small apps; consider PostgreSQL for production)
if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'aesl_db',
            'USER': 'aesl_user',
            'PASSWORD': 'christian@seer.com',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (very important for Vercel + WhiteNoise)
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "sourceEditing",
            "|",
            "heading",
            "|",
            "bold",
            "italic",
            "underline",
            "strikethrough",
            "|",
            "fontSize",
            "fontColor",
            "fontBackgroundColor",
            "|",
            "alignment",
            "|",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "outdent",
            "indent",
            "|",
            "link",
            "blockQuote",
            "insertTable",
            "imageUpload",
            "mediaEmbed",
            "|",
            "horizontalLine",
            "specialCharacters",
            "code",
            "codeBlock",
            "|",
            "findAndReplace",
            "selectAll",
            "|",
            "undo",
            "redo"
        ],
        "height": "500px",
    },
    "extends": {
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": [
            "sourceEditing",
            "|",
            "heading",
            "|",
            "bold",
            "italic",
            "underline",
            "link",
            "imageUpload",
            "|",
            "undo",
            "redo",
        ],
        "htmlSupport": {
            "allow": [
                {
                    "name": "div",
                    "classes": True,
                    "attributes": True,
                    "styles": True,
                },
                {
                    "name": "img",
                    "attributes": True,
                    "classes": True,
                    "styles": True,
                },
            ]
        },

        "image": {
            "toolbar": [
                "imageTextAlternative",
                "toggleImageCaption",
                "imageStyle:inline",
                "imageStyle:block",
                "imageStyle:side",
            ]
        },

        "height": 600,
    },
}

# Security (good choices – Vercel terminates SSL so these are safe)
SECURE_SSL_REDIRECT = not DEBUG  # Only in production
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https")  # Recommended for Vercel
