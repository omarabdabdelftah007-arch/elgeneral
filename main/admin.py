from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import (
    User, StudentProfile, TeacherSettings, HonorRoll, 
    Course, Lecture, Enrollment, Exam, Question
)

# ==========================================
# 1. إعدادات المستخدم والطلاب
# ==========================================

@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'is_student', 'is_staff')
    list_filter = ('is_student', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

@admin.register(StudentProfile)
class StudentProfileAdmin(ModelAdmin):
    list_display = ('user', 'grade', 'system', 'governorate', 'phone', 'is_active')
    list_filter = ('grade', 'system', 'governorate', 'is_active')
    search_fields = ('user__username', 'phone')

# ==========================================
# 2. إعدادات الموقع ولوحة الشرف
# ==========================================

@admin.register(TeacherSettings)
class TeacherSettingsAdmin(ModelAdmin):
    list_display = ('name',)

@admin.register(HonorRoll)
class HonorRollAdmin(ModelAdmin):
    list_display = ('student_name', 'rank_description')
    search_fields = ('student_name',)

# ==========================================
# 3. الكورسات والمحاضرات والاشتراكات
# ==========================================

class LectureInline(TabularInline):
    model = Lecture
    extra = 1

@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ('title', 'grade', 'system', 'created_at')
    list_filter = ('grade', 'system')
    search_fields = ('title',)
    inlines = [LectureInline]

@admin.register(Lecture)
class LectureAdmin(ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title',)

@admin.register(Enrollment)
class EnrollmentAdmin(ModelAdmin):
    list_display = ('student', 'course', 'is_active', 'allowed_lectures_count', 'expiry_date')
    list_filter = ('is_active', 'course')
    search_fields = ('student__username', 'course__title')

# ==========================================
# 4. الامتحانات والأسئلة
# ==========================================

class QuestionInline(TabularInline):
    model = Question
    extra = 1

@admin.register(Exam)
class ExamAdmin(ModelAdmin):
    list_display = ('title', 'course', 'lecture', 'is_comprehensive', 'duration_mins')
    list_filter = ('is_comprehensive', 'course')
    search_fields = ('title',)
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ('text', 'exam', 'correct_answer')
    list_filter = ('exam',)
    search_fields = ('text',)