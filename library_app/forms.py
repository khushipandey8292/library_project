from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from .models import BooKtable,Authortable,Borrow

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
        fields = ['book_name', 'book_cate', 'book_published_year','book_sr_no', 'authors']
        widgets = {
            'book_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book name'}),
            'book_published_year': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'book_cate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book category'}),
            'book_sr_no':forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter book serial number'}),
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



class Borrowform(forms.ModelForm):
    BookCategory = forms.CharField(disabled=True, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    BookSerialNo= forms.CharField(disabled=True, required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    BookName=forms.CharField(disabled=True,required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model=Borrow
        fields=['BookName','BookCategory','BookSerialNo','return_date','due_date']
        widgets={
                'return_date':forms.DateInput(attrs={'class':'form-control'}),
                'due_date':forms.TextInput(attrs={'class':'form-control'})       
        }

# class LikeForm(forms.ModelForm):
#     class Meta:
#         model = Like_db
#         fields = []


# class RatingForm(forms.ModelForm):
#     class Meta:
#         model = BooKtable
#         fields = ['rating']



class RatingForm(forms.Form):
    rating = forms.FloatField(
        min_value=0,
        max_value=5,
        widget=forms.NumberInput(attrs={'step': 0.1})
    )
