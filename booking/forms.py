from django import forms
from .models import Comment, Reserve, Contact


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'text form-control', 'placeholder': 'Fikrini bildir..', 'id': 'reply'}),
        required=True)

    class Meta:
        model = Comment
        fields = ("body",)


class ReserveForm(forms.ModelForm):
    date = forms.CharField(label='Tarix',
                           widget=forms.TextInput(attrs={'placeholder': 'Tarix / Saat*', 'type': 'datetime-local'}))
    full_name = forms.CharField(label='Ad və soyad', widget=forms.TextInput(attrs={'placeholder': 'Ad və soyad*'}))

    count_of_guest = forms.CharField(label='Qonaqların sayı', widget=forms.TextInput(
        attrs={'placeholder': 'Qonaqların sayı*', 'type': 'number'}))
    phone_number = forms.CharField(label='Əlaqə nömrəsi',
                                   widget=forms.TextInput(attrs={'placeholder': 'Əlaqə nömrəsi*', 'type': 'tel'}))
    passport_number = forms.CharField(label='Passport nömrəsi',
                                      widget=forms.TextInput(attrs={'placeholder': 'Passport nömrəsi*', }))
    notes = forms.CharField(label='Əlavə qeydlər',
                            widget=forms.Textarea(attrs={'placeholder': 'Əlavə qeydlər', 'rows': 10}))

    class Meta:
        model = Reserve
        exclude = ("user", "restaurant", "reserved")

    def __init__(self, *args, **kwargs):
        super(ReserveForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control  form-control-background-white"})

        self.fields["full_name"].required = True

        self.fields["count_of_guest"].required = True

        self.fields["phone_number"].required = True

        self.fields["date"].required = True

        self.fields["passport_number"].required = True


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
            self.fields[field].required = True
        self.fields['name'].widget.attrs.update({"placeholder": "Adınız*"})
        self.fields['email'].widget.attrs.update({"placeholder": "E-poçt ünvanınız*", "type": "email"})
        self.fields['phone'].widget.attrs.update({"placeholder": "Əlaqə nömrəniz*", "type":"tel"})
        self.fields['subject'].widget.attrs.update({"placeholder": "Başlıq*"})
        self.fields['message'].widget.attrs.update({"placeholder": "Müraciətiniz*", "rows": 6})
