from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError

from .models import Activities, Categories

class AddActivitiesForm(forms.ModelForm):
    category = forms.ModelChoiceField(label='Категория', queryset=Categories.objects.all())
    class Meta:
        model = Activities
        fields = ['title', 'description', 'category', 'date', 'time', 'duration', 'contact']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'duration': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'В минутах'}),
            'contact': forms.EmailInput(attrs={'class': 'form-input'}),
        }

    def clean_duration(self):
        duration_in_minutes = self.cleaned_data['duration']
        duration_in_seconds = duration_in_minutes * 60

        if duration_in_minutes < timedelta(minutes=30):
            raise ValidationError("Нельзя создать мероприятие меньше 30 минут")

        return duration_in_seconds

    def clean_title(self):
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789 - "
        code = 'russian'

        title = self.cleaned_data['title']
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны присутствовать только русские символы, дефис и пробел",
                code=code, params={"value": title})
        return title