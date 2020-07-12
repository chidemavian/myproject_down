from django import forms


exam = (('Select One', 'Select One'),
  ('JAMB PREP', 'JAMB PREP'),
  ('WAEC', 'WAEC'),('NECO', 'NECO'),
  ('GCE', 'GCE'),('NABTEB', 'NABTEB'),
  ('POST UTME', 'POST UTME'),('JUPEB', 'JUPEB'),
  ('IJMB', 'IJMB'),('JOINT PROMOTION EXAM', 'JOINT PROMOTION EXAM'),
  ('APTITUDE TEST', 'APTITUDE TEST'),('ENTRANCE EXAM', 'ENTRANCE EXAM'),
  ('RECRUITMENT EXAM', 'RECRUITMENT EXAM'),('SCREANING EXAM', 'SCREANING EXAM'),
  ('OTHER','OTHER'),
  )




class signupform(forms.Form):
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='E-mail',max_length=50)
    exam = forms.ChoiceField(label= 'Exam', choices = exam)
    password = forms.CharField(label="Password",widget=forms.PasswordInput,required = True)

      # def __init__(self, *args, **kwargs):
      #    super(loginform, self).__init__(*args, **kwargs)
      #    self.fields['username'].widget.attrs['class'] = 'loginTxtbox'




    def __init__(self, *args, **kwargs):
        super(signupform, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['class'] = 'loginTxtbox'


class loginform(forms.Form):
      email = forms.CharField(label="Email",required = True)
      password = forms.CharField(label="Password",widget=forms.PasswordInput,required = True)

      def __init__(self, *args, **kwargs):
         super(loginform, self).__init__(*args, **kwargs)
         self.fields['email'].widget.attrs['class'] = 'loginTxtbox'
         self.fields['password'].widget.attrs['class'] = 'loginTxtbox'