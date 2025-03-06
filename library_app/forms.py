from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from .models import BooKtable,Authortable

class SignupForm(UserCreationForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password(again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','email']
        widgets={'username':forms.TextInput(attrs={'class':'form-control'}),
                 'email':forms.EmailInput(attrs={'class':'form-control'}),
                 }

class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password=forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    

class BookForm(forms.ModelForm):
    authors = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Authors name'
        }),
        help_text="Enter multiple authors separated by commas."
    )

    class Meta:
        model = BooKtable
        fields = ['book_name', 'book_cate', 'book_published_year', 'authors']
        widgets = {
            'book_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book name'}),
            'book_published_year': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'book_cate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book category'}),
        }

    def clean_authors(self):
   
        data = self.cleaned_data['authors']
        author_names = [name.strip() for name in data.split(',') if name.strip()]  

        if not author_names:
            raise forms.ValidationError("Please enter at least one author.")

        authors = []
        for name in author_names:
            author, created = Authortable.objects.get_or_create(author_name=name)  
            authors.append(author)  

        return authors  


class RatingForm(forms.ModelForm):
    class Meta:
        model = BooKtable
        fields = ['rating']
        
        

        
