import os
from pathlib import Path

# بناء المسارات داخل المشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# إعدادات الأمان (تذكر تغييرها عند الرفع الفعلي أونلاين)
SECRET_KEY = 'django-insecure-kw&thiamc$*v)*6%&19o10j$3=$j-_y3en-uh2giyyb#ad8ilv'
DEBUG = False
ALLOWED_HOSTS = ['*']

# تعريف التطبيقات
INSTALLED_APPS = [
    'jazzmin',  # لوحة تحكم جازمين (يجب أن تكون قبل الأدمن)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',     # التطبيق الأساسي للمنصة
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

ROOT_URLCONF = 'general_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media', # ضروري جداً لعرض الفيديوهات والصور
            ],
        },
    },
]

WSGI_APPLICATION = 'general_platform.wsgi.application'

# قاعدة البيانات (SQLite حالياً للتطوير)
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
LANGUAGE_CODE = 'ar-eg' # اللغة العربية
TIME_ZONE = 'Africa/Cairo'
USE_I18N = True
USE_TZ = True

# --- إعدادات الملفات الثابتة (Static) والوسائط (Media) ---

# ملفات الـ CSS والـ JS والصور الثابتة للموقع
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ملفات الـ Media (الفيديوهات المرفوعة، صور المدرس، صور الكورسات)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# موديل المستخدم المخصص
AUTH_USER_MODEL = 'main.User'

# إعدادات التوجيه (Login/Logout)
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'home'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'