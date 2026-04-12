from django.contrib import admin
from django.contrib import messages
from .models import User, StudentProfile, ParentProfile, Course, Lecture, TeacherSettings, HonorRoll, Enrollment

# ==========================================
# 1. تخصيص صفحة تفعيل الطلاب (الأهم لك)
# ==========================================

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    # الخانات اللي هتظهر في الجدول من بره
    list_display = ['user', 'get_full_name', 'grade', 'phone', 'is_active', 'system', 'governorate']
    
    # فلاتر سريعة على الجنب (فلتر بالنشط، بالسنة، بالمحافظة)
    list_filter = ['is_active', 'grade', 'system', 'governorate']
    
    # البحث باسم المستخدم أو الرقم
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']
    
    # إمكانية تعديل الحالة (نشط/غير نشط) والسنة مباشرة من الجدول بدون دخول
    list_editable = ['is_active', 'grade']

    # --- الأكشن السحري: الموافقة على مجموعة طلاب بضغطة واحدة ---
    actions = ['approve_students', 'deactivate_students']

    @admin.action(description="✅ الموافقة على الطلاب المحددين")
    def approve_students(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"تم تفعيل {updated} طالب بنجاح! ⚔️", messages.SUCCESS)

    @admin.action(description="❌ إلغاء تفعيل الطلاب المحددين")
    def deactivate_students(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"تم إيقاف {updated} حساب بنجاح.", messages.WARNING)

    # فنكشن لإظهار الاسم الكامل للطالب في الجدول
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'اسم الطالب بالكامل'

# ==========================================
# 2. تخصيص صفحة الاشتراكات (تفعيل الشهور)
# ==========================================

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'allowed_lectures_count', 'is_active', 'expiry_date']
    list_filter = ['course', 'is_active']
    list_editable = ['allowed_lectures_count', 'is_active']
    search_fields = ['student__username', 'course__title']

# ==========================================
# 3. تسجيل باقي الموديلات بشكل بسيط
# ==========================================

admin.site.register(User)
admin.site.register(ParentProfile)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # عرض النظام في الجدول من بره
    list_display = ['title', 'grade', 'system', 'created_at']
    
    # إضافة فلتر بالنظام على الجنب
    list_filter = ['grade', 'system']
    
    search_fields = ['title']

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    ordering = ['course', 'order']

admin.site.register(TeacherSettings)
admin.site.register(HonorRoll)

# تخصيص عنوان لوحة الإدارة
admin.site.site_header = "لوحة قيادة الجنرال ⚔️"
admin.site.site_title = "أكاديمية الجنرال"
admin.site.index_title = "مرحباً بك في غرفة العمليات"