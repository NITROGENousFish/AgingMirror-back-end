# users/forms.py
from django import forms

# 表单类用以生成表单
class AddForm(forms.Form):
    id = forms.CharField()
    image = forms.FileField()
