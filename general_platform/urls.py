from django.contrib import admin
from django.urls import path
from main import views  # تأكد أن اسم التطبيق في مشروعك هو main
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. لوحة تحكم الإدارة (الأدمن)
    path('admin/', admin.site.urls),
    
    # 2. الصفحات الأساسية للمنصة
    path('', views.home, name='home'),
    path('general/', views.general, name='general'),
    
    # 3. صفحة عرض المحاضرة (تفاصيل الدرس)
    path('lecture/<int:lecture_id>/', views.lecture_detail, name='lecture_detail'),
    
    # 4. نظام الحسابات (تسجيل، دخول، خروج)
    path('register/', views.register_student, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]

# 5. تفعيل عرض ملفات الميديا (الفيديوهات والصور) أثناء التطوير
if settings.DEBUG:
    # ربط مسار MEDIA المخصص للفيديوهات والصور المرفوعة
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # ربط مسار STATIC لملفات الـ CSS والـ JS
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)