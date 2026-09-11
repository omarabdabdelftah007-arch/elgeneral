from django import forms
from .models import StudentProfile, User

class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="اسم المستخدم")
    password = forms.CharField(widget=forms.PasswordInput, label="كلمة السر")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="تأكيد كلمة السر")

    class Meta:
        model = StudentProfile
        # تم إزالة parent_phone من القائمة هنا
        fields = ['grade', 'system', 'governorate', 'phone']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("كلمتا السر غير متطابقتين")
        return cleaned_data