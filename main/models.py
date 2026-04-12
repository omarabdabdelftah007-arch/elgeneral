import re
from django.db import models
from django.contrib.auth.models import AbstractUser

# ==========================================
# 1. موديلات المستخدمين والبروفايلات
# ==========================================

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)

class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    
    def __str__(self):
        return f"ولي أمر: {self.user.username}"

class StudentProfile(models.Model):
    GRADES = [
        ('1', 'الصف الأول الثانوي'),
        ('2', 'الصف الثاني الثانوي'),
        ('3', 'الصف الثالث الثانوي')
    ]
    SYSTEMS = [
        ('general', 'عام'),
        ('azhar', 'أزهري')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    parent = models.ForeignKey(ParentProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    
    grade = models.CharField(max_length=20, choices=GRADES, verbose_name="السنة الدراسية")
    system = models.CharField(max_length=20, choices=SYSTEMS, verbose_name="النظام")
    governorate = models.CharField(max_length=50, verbose_name="المحافظة")
    phone = models.CharField(max_length=15, verbose_name="رقم الطالب")
    parent_phone = models.CharField(max_length=15, verbose_name="رقم ولي الأمر")
    
    is_active = models.BooleanField(default=False, verbose_name="تم تفعيل الحساب")

    class Meta:
        verbose_name = "بروفايل طالب"
        verbose_name_plural = "بروفايلات الطلاب"

    def __str__(self):
        return self.user.username

# ==========================================
# 2. إعدادات "الجنرال" (التحكم في الصفحة الرئيسية)
# ==========================================

class TeacherSettings(models.Model):
    name = models.CharField(max_length=100, default="الأستاذ محمد عيد")
    main_image = models.ImageField(upload_to='teacher_info/', help_text="ارفع صورة المستر الكبيرة هنا")
    
    # هنا التعديل: فيديو الصفحة الرئيسية فقط أصبح ملفاً مرفوعاً
    intro_video = models.FileField(
        upload_to='teacher_videos/', 
        null=True, 
        blank=True, 
        help_text="ارفع الفيديو التعريفي من جهازك مباشرة (MP4)"
    )
    
    philosophical_quote = models.TextField(default="الفلسفة ليست مادة تحفظ، بل هي عقل يفكر وحياة تُعاش.")
    
    class Meta:
        verbose_name = "إعدادات الجنرال (الرئيسية)"
        verbose_name_plural = "إعدادات الجنرال (الرئيسية)"

    def __str__(self):
        return self.name

class HonorRoll(models.Model):
    student_name = models.CharField(max_length=150)
    rank_description = models.CharField(max_length=200, help_text="مثال: الأولى على محافظة كفر الشيخ")
    image = models.ImageField(upload_to='honor_roll/', blank=True, null=True, help_text="اختياري: صورة الطالب")

    class Meta:
        verbose_name = "لوحة الشرف"
        verbose_name_plural = "لوحة الشرف"

# ==========================================
# 3. الكورسات والمحاضرات (رجعت يوتيوب كما كانت)
# ==========================================

SYSTEM_CHOICES = [
    ('general', 'عام'),
    ('azhar', 'أزهري'),
    ('bac', 'بكالوريا'),
    ('all', 'الكل (عام وأزهري وبكالوريا)')
]

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="اسم الكورس (مثلاً: شهر أكتوبر)")
    grade = models.CharField(max_length=2, choices=StudentProfile.GRADES, verbose_name="مخصص لسنة")
    system = models.CharField(
        max_length=10, 
        choices=SYSTEM_CHOICES, 
        default='all', 
        verbose_name="مخصص لنظام"
    )
    description = models.TextField(verbose_name="وصف محتوى الشهر")
    image = models.ImageField(upload_to='course_images/', blank=True, null=True, verbose_name="غلاف الكورس")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "كورس / شهر"
        verbose_name_plural = "الكورسات (الشهور)"

    def __str__(self):
        return f"[{self.get_grade_display()}] - {self.title}"

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=200, verbose_name="عنوان المحاضرة")
    
    # رجعت URLField كما طلبت لسهولة الاستخدام مع يوتيوب
    video_url = models.URLField(help_text="رابط فيديو اليوتيوب") 
    
    pdf_file = models.FileField(upload_to='lectures_pdf/', blank=True, null=True, verbose_name="ملف PDF للمحاضرة")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتيب المحاضرة")

    def get_embed_url(self):
        url = self.video_url.strip()
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=|shorts/)?([^&=%\?]{11})'
        match = re.match(youtube_regex, url)
        if match:
            video_id = match.group(6)
            return f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1"
        return url

    class Meta:
        ordering = ['order']
        verbose_name = "محاضرة"
        verbose_name_plural = "المحاضرات"

    def __str__(self):
        return f"{self.course.title} - {self.title}"

# ==========================================
# 4. نظام الاشتراكات
# ==========================================

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolled_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="الكورس (الشهر)")
    is_active = models.BooleanField(default=True, verbose_name="الاشتراك مفعل")
    allowed_lectures_count = models.PositiveIntegerField(default=1, verbose_name="عدد المحاضرات المفتوحة له")
    expiry_date = models.DateField(null=True, blank=True, verbose_name="تاريخ انتهاء الاشتراك")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')
        verbose_name = "اشتراك طالب"
        verbose_name_plural = "اشتراكات الطلاب"

    def __str__(self):
        return f"{self.student.username} -> {self.course.title}"