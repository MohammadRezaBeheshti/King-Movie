from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(attrs={
            "class": "w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-4 py-3 text-sm text-[var(--foreground)] placeholder:text-[var(--muted-foreground)]/50 focus:border-[var(--primary)] focus:ring-2 focus:ring-[var(--primary)]/20 outline-none transition duration-200",
            "placeholder": "نام کاربری خود را وارد کنید",
            "autofocus": True,
        }),
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={
            "class": "w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-4 py-3 text-sm text-[var(--foreground)] placeholder:text-[var(--muted-foreground)]/50 focus:border-[var(--primary)] focus:ring-2 focus:ring-[var(--primary)]/20 outline-none transition duration-200",
            "placeholder": "رمز عبور خود را وارد کنید",
        }),
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="ایمیل (اختیاری)",
        required=False,
        widget=forms.EmailInput(attrs={
            "placeholder": "name@example.com",
        }),
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "نام کاربری"
        self.fields["password1"].label = "رمز عبور"
        self.fields["password2"].label = "تکرار رمز عبور"
        self.fields["email"].label = "ایمیل (اختیاری)"
        self.fields["username"].widget.attrs.setdefault("placeholder", "نام کاربری مورد نظر")
        self.fields["password1"].widget.attrs.setdefault("placeholder", "حداقل ۸ کاراکتر")
        self.fields["password2"].widget.attrs.setdefault("placeholder", "تکرار رمز عبور")

        input_classes = "w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-4 py-3 text-sm text-[var(--foreground)] placeholder:text-[var(--muted-foreground)]/50 focus:border-[var(--primary)] focus:ring-2 focus:ring-[var(--primary)]/20 outline-none transition duration-200"

        for field in self.fields.values():
            field.widget.attrs["class"] = input_classes