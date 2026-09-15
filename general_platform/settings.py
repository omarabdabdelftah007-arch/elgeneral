import os
from pathlib import Path

# بناء المسارات داخل المشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# إعدادات الأمان
SECRET_KEY = 'django-insecure-kw&thiamc$*v)*6%&19o10j$3=$j-_y3en-uh2giyyb#ad8ilv'
DEBUG = True
ALLOWED_HOSTS = ['*']

# تحديث النطاقات الموثوقة لمنع خطأ CSRF محلياً وعلى السيرفر
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:*',
    'http://localhost:8000',
    'http://localhost:3000',
    'http://localhost:*',
    'https://elgeneeral.online',
    'https://www.elgeneeral.online',
    'http://elgeneeral.online',
    'http://www.elgeneeral.online',
]

# إعدادات جلسات الكوكيز للتطوير المحلي
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# تعريف التطبيقات (Unfold قبل django.contrib.admin)
INSTALLED_APPS = [
    'unfold',  # لوحة تحكم Unfold
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',    # التطبيق الأساسي للمنصة
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'general_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # تم التصحيح هنا
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'general_platform.wsgi.application'

# قاعدة البيانات (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# التحقق من كلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# الإعدادات الإقليمية
LANGUAGE_CODE = 'ar-eg'
TIME_ZONE = 'Africa/Cairo'
USE_I18N = True
USE_TZ = True

# --- إعدادات الملفات الثابتة (Static) والوسائط (Media) ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# موديل المستخدم المخصص
AUTH_USER_MODEL = 'main.User'

# إعدادات التوجيه (Login/Logout)
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'home'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'