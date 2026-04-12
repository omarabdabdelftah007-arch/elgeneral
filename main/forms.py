from django import forms
from .models import User, StudentProfile

class StudentRegistrationForm(forms.ModelForm):
    # --- بيانات حساب الطالب ---
    username = forms.CharField(
        max_length=150, 
        label="اسم مستخدم الطالب",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المستخدم'})
    )
    email = forms.EmailField(
        label="إيميل الطالب",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'})
    )
    password = forms.CharField(
        label="كلمة سر الطالب",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'كلمة السر'})
    )
    
    # --- بيانات حساب ولي الأمر ---
    parent_username = forms.CharField(
        max_length=150, 
        label="اسم مستخدم ولي الأمر",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم مستخدم للأب'})
    )
    parent_email = forms.EmailField(
        label="إيميل ولي الأمر",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'parent@example.com'})
    )
    parent_password = forms.CharField(
        label="كلمة سر ولي الأمر",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'كلمة سر ولي الأمر'})
    )

    class Meta:
        model = StudentProfile
        # الخانات اللي في الموديل عندك
        fields = ['grade', 'system', 'governorate', 'phone', 'parent_phone']
        labels = {
            'grade': 'الصف الدراسي',
            'system': 'النظام التعليمي',
            'governorate': 'المحافظة',
            'phone': 'رقم تليفون الطالب',
            'parent_phone': 'رقم تليفون ولي الأمر',
        }
        widgets = {
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'system': forms.Select(attrs={'class': 'form-control'}),
            'governorate': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # دالة للتأكد إن الـ Username مش مكرر (عشان السيرفر ما يضربش Error)
    def clean(self):
        cleaned_data = super().clean()
        user_name = cleaned_data.get("username")
        p_user_name = cleaned_data.get("parent_username")

        if User.objects.filter(username=user_name).exists():
            self.add_error('username', "اسم المستخدم ده محجوز لطالب آخر.")
        
        if User.objects.filter(username=p_user_name).exists():
            self.add_error('parent_username', "اسم المستخدم ده محجوز لولي أمر آخر.")
            
        return cleaned_data