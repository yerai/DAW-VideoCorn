from django.contrib.auth.models import User
from django.forms import ModelForm

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'