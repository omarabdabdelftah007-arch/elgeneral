from django import forms
from .models import StudentProfile, User

class StudentRegistrationForm(forms.ModelForm):
    # حقول إنشاء حساب الـ User الأساسي
    username = forms.CharField(max_length=150, label="اسم المستخدم")
    password = forms.CharField(widget=forms.PasswordInput, label="كلمة السر")

    class Meta:
        model = StudentProfile
        fields = ['full_name', 'phone', 'parent_phone', 'grade', 'system', 'governorate']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("اسم المستخدم مستخدم بالفعل، اختر اسماً آخر.")
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if StudentProfile.objects.filter(phone=phone).exists():
            raise forms.ValidationError("رقم الهاتف هذا مسجل بالفعل بحساب آخر.")
        return phone


class LoginForm(forms.Form):
    # حقل موحد يقبل رقم الهاتف أو اسم المستخدم
    username_or_phone = forms.CharField(
        label="اسم المستخدم أو رقم الهاتف",
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'اسم المستخدم أو رقم الموبايل'})
    )
    password = forms.CharField(
        label="كلمة السر",
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )