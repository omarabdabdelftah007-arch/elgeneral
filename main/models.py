import re
from django.db import models
from django.contrib.auth.models import AbstractUser

# ==========================================
# 1. موديلات المستخدمين والبروفايلات
# ==========================================

class User(AbstractUser):
    is_student = models.BooleanField(default=True)

class StudentProfile(models.Model):
    GRADES = [
        ('1', 'الصف الأول الثانوي'),
        ('2', 'الصف الثاني الثانوي'),
        ('3', 'الصف الثالث الثانوي')
    ]
    SYSTEMS = [
        ('general', 'عام'),
        ('azhar', 'أزهري'),
        ('bakaloria', 'بكالوريا')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    grade = models.CharField(max_length=20, choices=GRADES, verbose_name="السنة الدراسية")
    system = models.CharField(max_length=20, choices=SYSTEMS, verbose_name="النظام")
    governorate = models.CharField(max_length=50, verbose_name="المحافظة")
    phone = models.CharField(max_length=15, verbose_name="رقم الطالب")
    
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
# 3. الكورسات والمحاضرات
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

# ==========================================
# 5. الامتحانات والأسئلة
# ==========================================

class Exam(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان الامتحان")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name='exams', verbose_name="التابع لكورس")
    lecture = models.ForeignKey(Lecture, on_delete=models.SET_NULL, blank=True, null=True, related_name='exams', verbose_name="تابع لمحاضرة (اختياري)")
    is_comprehensive = models.BooleanField(default=False, verbose_name="امتحان شامل؟")
    duration_mins = models.IntegerField(default=30, verbose_name="مدة الامتحان بالدقائق")

    class Meta:
        verbose_name = "امتحان"
        verbose_name_plural = "📝 الامتحانات"

    def __str__(self):
        return self.title

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions', verbose_name="الامتحان")
    text = models.TextField(verbose_name="نص السؤال")
    image = models.ImageField(upload_to='questions_images/', blank=True, null=True, verbose_name="صورة مع السؤال (اختياري)")
    choice1 = models.CharField(max_length=255, verbose_name="الاختيار الأول")
    choice2 = models.CharField(max_length=255, verbose_name="الاختيار الثاني")
    choice3 = models.CharField(max_length=255, verbose_name="الاختيار الثالث")
    choice4 = models.CharField(max_length=255, verbose_name="الاختيار الرابع")

    CORRECT_ANSWER_CHOICES = [
        ('1', 'الاختيار الأول'),
        ('2', 'الاختيار الثاني'),
        ('3', 'الاختيار الثالث'),
        ('4', 'الاختيار الرابع'),
    ]
    correct_answer = models.CharField(max_length=1, choices=CORRECT_ANSWER_CHOICES, verbose_name="الإجابة الصحيحة")

    class Meta:
        verbose_name = "سؤال"
        verbose_name_plural = "❓ الأسئلة"

    def __str__(self):
        return f"سؤال في: {self.exam.title}"