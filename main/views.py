from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm
from .models import User, ParentProfile, StudentProfile, Course, Lecture, TeacherSettings, HonorRoll, Enrollment

# ==========================================
# 1. صفحة التسجيل (ربط الطالب بولي الأمر)
# ==========================================
def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # إنشاء حساب ولي الأمر
                parent_user = User.objects.create_user(
                    username=form.cleaned_data['parent_username'],
                    email=form.cleaned_data['parent_email'],
                    password=form.cleaned_data['parent_password'],
                    is_parent=True,
                    is_student=False
                )
                parent_profile = ParentProfile.objects.create(user=parent_user)

                # إنشاء حساب الطالب
                student_user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    is_student=True,
                    is_parent=False
                )
                
                student_profile = form.save(commit=False)
                student_profile.user = student_user
                student_profile.parent = parent_profile
                # الحساب يكون غير مفعل (is_active=False) حتى يوافق الجنرال من الأدمن
                student_profile.is_active = False 
                student_profile.save()

                return redirect('login')
            except Exception as e:
                print(f"Error during registration: {e}")
        else:
            print("Form Errors:", form.errors)
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

# ==========================================
# 2. الصفحة الرئيسية (عرض عام)
# ==========================================
def home(request):
    teacher = TeacherSettings.objects.first()
    honor_students = HonorRoll.objects.all()
    # في الرئيسية نعرض عينة من الكورسات فقط للتشويق
    courses = Course.objects.all()[:3] 
    
    context = {
        'teacher': teacher,
        'honor_students': honor_students,
        'courses': courses
    }
    return render(request, "home.html", context)

# ==========================================
# 3. صفحة الكورسات (نظام الحماية والاشتراكات 🛡️)
# ==========================================
@login_required(login_url='login')
def general(request):
    # 1. لو ولي أمر، نوجهه لصفحة تانية أو الرئيسية (لأن الكورسات للطلبة)
    if request.user.is_parent:
        return render(request, "parent_dashboard.html", {'message': "هذه الصفحة مخصصة للطلاب فقط."})
    
    # 2. التحقق من تفعيل حساب الطالب بواسطة الجنرال
    if not request.user.is_staff:
        if hasattr(request.user, 'student_profile'):
            if not request.user.student_profile.is_active:
                # لو الطالب لسه متمش تفعيله، يروح لصفحة الانتظار
                return render(request, "waiting_activation.html")
        else:
            return redirect('home')

   # 3. منطق عرض الكورسات المسموحة فقط
    student_profile = request.user.student_profile

    # جلب الـ IDs الخاصة بالكورسات اللي الطالب دفع ثمنها "ومفعلة" له
    allowed_course_ids = Enrollment.objects.filter(
        student=request.user,
        is_active=True
    ).values_list('course_id', flat=True)

    # فلترة الكورسات بناءً على: (أن يكون الطالب مشتركاً فيها + أن تكون من نفس سنته الدراسية)
    courses = Course.objects.filter(
        id__in=allowed_course_ids,
        grade=student_profile.grade
    )

    # --- ملاحظة للجنرال ---
    # لو عايز الكورسات تظهر لكل طلبة السنة الدراسية (حتى اللي مدفعوش) كعرض فقط:
    # امسح سطر id__in=allowed_course_ids وسيب grade=student_profile.grade بس.
    # ----------------------

    return render(request, "general.html", {
        'courses': courses,
        'student': student_profile
    })

# ==========================================
# 4. تفاصيل المحاضرة (تأمين المشاهدة)
# ==========================================
@login_required(login_url='login')
def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    course = lecture.course
    
    # تأمين الفيديو: التأكد إن الطالب مشترك في "الكورس" التابع له هذه المحاضرة
    if not request.user.is_staff:
        is_enrolled = Enrollment.objects.filter(
            student=request.user, 
            course=course, 
            is_active=True
        ).exists()
        
        if not is_enrolled:
            return redirect('general') # لو مش مشترك يرجعه لصفحة الكورسات
                
    return render(request, 'lecture_detail.html', {'lecture': lecture})

# ==========================================
# 5. تسجيل الخروج
# ==========================================
def logout_view(request):
    logout(request)
    return redirect('home')