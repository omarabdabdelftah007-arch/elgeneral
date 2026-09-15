from django.contrib import admin
from django.urls import path
from main import views  # تطبيق main
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
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signout/', views.logout_view, name='signout'),  # مسار منفصل لتفادي أخطاء القوالب القديمة
    
    # 5. الامتحانات والنتائج
    path('exams/', views.exams_view, name='exams'),
    path('exam/<int:exam_id>/take/', views.take_exam, name='take_exam'),       # مسار بدء ودخول الامتحان
    path('exam/<int:exam_id>/result/', views.exam_result_view, name='exam_result'), # مسار نتيجة الامتحان
]

# تفعيل عرض ملفات الميديا (الفيديوهات والصور) والـ Static أثناء التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)