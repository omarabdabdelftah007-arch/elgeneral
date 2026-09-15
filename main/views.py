from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, LoginForm
from .models import (
    User, StudentProfile, Course, 
    Lecture, TeacherSettings, HonorRoll, Enrollment, 
    Exam
)

# ==========================================
# 1. صفحة التسجيل 📝
# ==========================================
def register_student(request):
    error_message = None

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                
                # التحقق المباشر من عدم تكرار اسم المستخدم
                if User.objects.filter(username=username).exists():
                    error_message = "اسم المستخدم مستخدم بالفعل، اختر اسماً آخر."
                else:
                    # 1. إنشاء حساب المستخدم الأساسي
                    student_user = User.objects.create_user(
                        username=username,
                        password=form.cleaned_data['password'],
                        is_student=True
                    )
                    
                    # 2. إنشاء ملف البروفايل للطالب
                    StudentProfile.objects.create(
                        user=student_user,
                        full_name=form.cleaned_data.get('full_name', ''),
                        phone=form.cleaned_data.get('phone', ''),
                        parent_name=form.cleaned_data.get('parent_name', ''),
                        parent_phone=form.cleaned_data.get('parent_phone', ''),
                        grade=form.cleaned_data.get('grade'),
                        system=form.cleaned_data.get('system'),
                        governorate=form.cleaned_data.get('governorate', ''),
                        is_active=True
                    )

                    # 3. تسجيل الدخول المباشر مع تحديد الـ Backend
                    login(request, student_user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('general')
                    
            except Exception as e:
                error_message = f"حدث خطأ أثناء حفظ البيانات: {e}"
        else:
            # استخراج أسباب عدم صحة البيانات من الـ Form
            first_error_field = list(form.errors.keys())[0]
            error_text = form.errors[first_error_field][0]
            error_message = f"خطأ في حقل ({first_error_field}): {error_text}"
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'register.html', {
        'form': form,
        'error_message': error_message
    })

# ==========================================
# 2. صفحة تسجيل الدخول (تسجيل باسم المستخدم أو الهاتف) 🔐
# ==========================================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('general')

    error_message = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data['username_or_phone'].strip()
            password = form.cleaned_data['password']

            username_to_auth = login_input

            # إذا أدخل الطالب أرقام فقط، نبحث عن الحساب المرتبط بهذا الرقم
            if login_input.isdigit():
                profile = StudentProfile.objects.filter(phone=login_input).first()
                if profile:
                    username_to_auth = profile.user.username

            # مصادقة الحساب
            user = authenticate(request, username=username_to_auth, password=password)

            if user is not None:
                login(request, user)
                return redirect('general')
            else:
                error_message = "اسم المستخدم / رقم الهاتف أو كلمة السر غير صحيحة."
        else:
            error_message = "يرجى التأكد من ملء جميع البيانات."
    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form,
        'error_message': error_message
    })

# ==========================================
# 3. الصفحة الرئيسية (عرض عام) 🏠
# ==========================================
def home(request):
    teacher = TeacherSettings.objects.first()
    honor_students = HonorRoll.objects.all()
    courses = Course.objects.all()[:3] 
    
    context = {
        'teacher': teacher,
        'honor_students': honor_students,
        'courses': courses
    }
    return render(request, "home.html", context)

# ==========================================
# 4. صفحة الكورسات (نظام الحماية والاشتراكات 🛡️)
# ==========================================
@login_required(login_url='login')
def general(request):
    if not request.user.is_staff:
        if hasattr(request.user, 'student_profile'):
            if not request.user.student_profile.is_active:
                return render(request, "waiting_activation.html")
        else:
            return redirect('home')

    student_profile = getattr(request.user, 'student_profile', None)

    if student_profile:
        allowed_course_ids = Enrollment.objects.filter(
            student=request.user,
            is_active=True
        ).values_list('course_id', flat=True)

        courses = Course.objects.filter(
            id__in=allowed_course_ids,
            grade=student_profile.grade
        )
    else:
        courses = Course.objects.all()

    return render(request, "general.html", {
        'courses': courses,
        'student': student_profile
    })

# ==========================================
# 5. تفاصيل المحاضرة (تأمين المشاهدة) 🎥
# ==========================================
@login_required(login_url='login')
def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    course = lecture.course
    
    if not request.user.is_staff:
        is_enrolled = Enrollment.objects.filter(
            student=request.user, 
            course=course, 
            is_active=True
        ).exists()
        
        if not is_enrolled:
            return redirect('general')
                
    return render(request, 'lecture_detail.html', {'lecture': lecture})

# ==========================================
# 6. تسجيل الخروج 🚪
# ==========================================
def logout_view(request):
    logout(request)
    return redirect('home')

# ==========================================
# 7. صفحة الامتحانات 📋
# ==========================================
@login_required(login_url='login')
def exams_view(request):
    student_profile = getattr(request.user, 'student_profile', None)
    
    if not student_profile:
        if request.user.is_staff:
            exams_list = Exam.objects.all()
            return render(request, 'exams.html', {'exams': exams_list})
        else:
            return redirect('home')

    student_grade = student_profile.grade

    subscribed_courses = Enrollment.objects.filter(
        student=request.user,
        is_active=True
    ).values_list('course_id', flat=True)

    exams_list = Exam.objects.filter(
        course__grade=student_grade,
        course_id__in=subscribed_courses
    )

    return render(request, 'exams.html', {'exams': exams_list})

# ==========================================
# 8. صفحة تقديم الامتحان ⏱️
# ==========================================
@login_required(login_url='login')
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    
    if request.method == 'POST':
        score = 0
        for question in questions:
            selected_choice = request.POST.get(f'question_{question.id}')
            if selected_choice and selected_choice == str(question.correct_answer):
                score += 1
                
        request.session[f'exam_{exam.id}_score'] = score
        return redirect('exam_result', exam_id=exam.id)
        
    return render(request, 'take_exam.html', {
        'exam': exam,
        'questions': questions
    })

# ==========================================
# 9. صفحة عرض نتيجة الامتحان 📊
# ==========================================
@login_required(login_url='login')
def exam_result_view(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    score = request.session.get(f'exam_{exam_id}_score', 0)
    questions_qs = getattr(exam, 'questions', None)
    total = questions_qs.count() if questions_qs else 0
    percentage = round((score / total * 100), 1) if total > 0 else 0

    context = {
        'exam': exam,
        'score': score,
        'total': total,
        'percentage': percentage,
    }
    return render(request, 'exam_result.html', context)