from django import forms

from .models import Rating, Review


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["score"]
        widgets = {
            "score": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 10,
                    "class": "w-full rounded-lg border border-[var(--border)] bg-[var(--surface)] px-3 py-2 text-sm text-[var(--foreground)] outline-none focus:border-[var(--primary)] focus:ring-2 focus:ring-[var(--primary)]/20",
                }
            ),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "w-full resize-y rounded-lg border border-[var(--border)] bg-[var(--surface)] px-3 py-3 text-sm leading-7 text-[var(--foreground)] outline-none placeholder:text-[var(--foreground)]/35 focus:border-[var(--primary)] focus:ring-2 focus:ring-[var(--primary)]/20",
                    "placeholder": "نظر خود را درباره این عنوان بنویسید...",
                }
            ),
        }
