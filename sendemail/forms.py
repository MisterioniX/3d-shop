from django import forms


class EmailForm(forms.Form):
    """EmailForm definition."""

    # TODO: Define form fields here
    
    subject = forms.CharField(label='Тема', required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    message = forms.CharField(label='Сообщение', required=True, widget=forms.Textarea(attrs={
        'class': 'form-control', 
    }))
