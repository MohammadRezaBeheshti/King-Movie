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
                    "class": "w-full rounded-lg border border-white/10 bg-black/30 px-3 py-2 text-sm text-white outline-none focus:border-[#eab308]/70 focus:ring-2 focus:ring-[#eab308]/20",
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
                    "class": "w-full resize-y rounded-lg border border-white/10 bg-black/30 px-3 py-3 text-sm leading-7 text-white outline-none placeholder:text-white/35 focus:border-[#eab308]/70 focus:ring-2 focus:ring-[#eab308]/20",
                    "placeholder": "نظر خود را درباره این عنوان بنویسید...",
                }
            ),
        }
