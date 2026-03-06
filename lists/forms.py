from django import forms
from .models import Task

class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title','body','due_date')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class':'form-control','rows':4}),
            'due_date': forms.DateInput(attrs={
                'type':'date',
                'class':'form-control'
            }),      
        }
        
class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title','body','is_done','due_date')

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class':'form-control','rows':4}),
            'is_done': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'due_date': forms.DateInput(attrs={
                'type':'date',
                'class':'form-control'
            }),
        }