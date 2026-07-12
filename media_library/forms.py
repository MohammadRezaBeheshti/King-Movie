from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(required=False)
    type = forms.ChoiceField(required=False)
    genre = forms.ChoiceField(required=False)
    country = forms.ChoiceField(required=False)
    year_from = forms.IntegerField(required=False, min_value=1888)
    year_to = forms.IntegerField(required=False, min_value=1888)
    rating = forms.DecimalField(required=False, min_value=1, max_value=10, max_digits=3, decimal_places=1)
    status = forms.ChoiceField(required=False)
    director = forms.ChoiceField(required=False)
    actor = forms.ChoiceField(required=False)
    sort = forms.ChoiceField(required=False)

    def __init__(self, *args, filter_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        filter_choices = filter_choices or {}

        self.fields["type"].choices = filter_choices.get("media_types", [])
        self.fields["genre"].choices = filter_choices.get("genres", [])
        self.fields["country"].choices = filter_choices.get("countries", [])
        self.fields["status"].choices = filter_choices.get("statuses", [])
        self.fields["director"].choices = filter_choices.get("directors", [])
        self.fields["actor"].choices = filter_choices.get("actors", [])
        self.fields["sort"].choices = filter_choices.get("sorts", [])

        common_input_class = (
            "w-full rounded-lg border border-[var(--border)] bg-[var(--card)] px-3 py-2 "
            "text-sm text-[var(--foreground)] outline-none transition placeholder:text-[var(--foreground)]/35 "
            "focus:border-[var(--primary)] focus:ring-2 focus:ring-[var(--primary)]/20"
        )
        common_select_class = (
            "w-full rounded-lg border border-[var(--border)] bg-[var(--card)] px-3 py-2 "
            "text-sm text-[var(--foreground)] outline-none transition focus:border-[var(--primary)] "
            "focus:ring-2 focus:ring-[var(--primary)]/20"
        )

        placeholders = {
            "q": "نام فارسی، انگلیسی یا اصلی...",
            "year_from": "از سال",
            "year_to": "تا سال",
            "rating": "حداقل امتیاز IMDb",
        }

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({"class": common_select_class})
            else:
                field.widget.attrs.update({
                    "class": common_input_class,
                    "placeholder": placeholders.get(name, ""),
                })
