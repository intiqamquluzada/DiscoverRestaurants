from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from booking.models import Restaurants, RestaurantMenu, RestaurantImages

User = get_user_model()
CHOICES = (
    ("Kişi", "Kişi"),
    ("Qadın", "Qadın")

)


# -----------------------   Admin Forms  ---------------------------------------------------

class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name', 'surname', 'password1', 'password2')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'name', 'surname', 'password', 'is_active', 'is_superuser', 'is_restaurant_owner')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class RegistrationUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Şifrə', widget=forms.PasswordInput(attrs={"placeholder": "Şifrə"}))
    password2 = forms.CharField(label='Təkrar şifrə', widget=forms.PasswordInput(attrs={"placeholder": "Təkrar şifrə"}))
    gender = forms.ChoiceField(label='Cinsiyyət', choices=CHOICES, )
    phone = forms.CharField(label="Əlaqə nömrəsi",
                            widget=forms.TextInput(attrs={"type": "tel", "placeholder": "+994XXXXXXXXX"}))

    class Meta:
        model = User
        fields = ("name", "surname", "email", "phone", "gender", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegistrationUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control form-control-lg"})
            self.fields[field].required = True
        self.fields["name"].widget.attrs.update({"placeholder": "Adınızı daxil edin"})
        self.fields["surname"].widget.attrs.update({"placeholder": "Soyadınızı daxil edin"})
        self.fields["email"].widget.attrs.update({"placeholder": "E-poçtunuzu daxil edin"})
        self.fields["phone"].widget.attrs.update({"placeholder": "Əlaqə nömrənizi daxil edin"})

    def clean(self):
        email = self.cleaned_data.get("email")
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        phone = self.cleaned_data.get("phone")

        for n in phone:
            if n.isalpha():
                raise forms.ValidationError("Nömrəni düzgün daxil edin")

        if not (password1 and password2 and password1 == password2):
            raise forms.ValidationError("Şifrələr uyğun deyil")

        if len(password1) < 8:
            raise forms.ValidationError("Şifrənin uzunluğu minimum 8 simvoldan ibarət olmalıdır.")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-poçtla hesab mövcuddur")

        return self.cleaned_data


class RegisterOwnerForm(forms.ModelForm):
    restaurant_images = forms.FileField(label="Restoran şəkilləri əlavə et",
                                        widget=forms.ClearableFileInput(attrs={"multiple": True}))
    menu_images = forms.FileField(label="Menyu şəkilləri əlavə et",
                                  widget=forms.ClearableFileInput(attrs={"multiple": True}))

    class Meta:
        model = Restaurants
        fields = ("name", "type_r", "country_of_restaurant",
                  "city", "number", "location",
                  "available_seats", "description",)

    def __init__(self, *args, **kwargs):
        super(RegisterOwnerForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields['name'].label = "Restoranın adı"
        self.fields['name'].widget.attrs.update({"placeholder": "Restoranın adı"})
        self.fields['type_r'].label = "Restoranın tipi"
        self.fields['country_of_restaurant'].label = "Restoranın yerləşdiyi ölkə"
        self.fields['city'].label = "Restoranın yerləşdiyi şəhər"
        self.fields['city'].widget.attrs.update({"placeholder": "Bakı, Ganja və s."})
        self.fields['number'].label = "Restoranın əlaqə nömrəsi"
        self.fields['number'].widget.attrs.update({"placeholder": "Əlaqə nömrəsi, məs: +994XXXXXXXXX"})
        self.fields['location'].label = "Ünvan"
        self.fields['location'].widget.attrs.update({"placeholder": "Nakchivani 10"})
        self.fields['available_seats'].label = "Uyğun yerlər"
        self.fields['description'].label = "Restoran haqqında məlumat"
        self.fields['description'].widget.attrs.update({
            "placeholder": "Restoranımızın özünə məxsus bir sıra üstünlükləri vardır. Eyvan və şəhər görünümlü yerləşim qonaqlarımızın bizi tərcih etməyinin birinci səbəbidir və s......"})


class OwnerUpdateForm(forms.ModelForm):
    class Meta:
        model = Restaurants
        fields = ("name", "type_r", "country_of_restaurant",
                  "city", "number", "location",
                  "available_seats", "description",)

    def __init__(self, *args, **kwargs):
        super(OwnerUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
            self.fields[field].required = True
        self.fields['name'].label = "Restoranın adı"
        self.fields['name'].widget.attrs.update({"placeholder": "Restoranın adı"})
        self.fields['type_r'].label = "Restoranın tipi"
        self.fields['country_of_restaurant'].label = "Restoranın yerləşdiyi ölkə"
        self.fields['city'].label = "Restoranın yerləşdiyi şəhər"
        self.fields['city'].widget.attrs.update({"placeholder": "Bakı, Ganja və s."})
        self.fields['number'].label = "Restoranın əlaqə nömrəsi"
        self.fields['number'].widget.attrs.update({"placeholder": "Əlaqə nömrəsi, məs: +994XXXXXXXXX"})
        self.fields['location'].label = "Ünvan"
        self.fields['location'].widget.attrs.update({"placeholder": "Nakchivani 10"})
        self.fields['available_seats'].label = "Uyğun yerlər"
        self.fields['description'].label = "Restoran haqqında məlumat"
        self.fields['description'].widget.attrs.update({
            "placeholder": "Restoranımızın özünə məxsus bir sıra üstünlükləri vardır. Eyvan və şəhər görünümlü yerləşim qonaqlarımızın bizi tərcih etməyinin birinci səbəbidir və s......"})


class UserForgetEmail(forms.Form):

    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "type": "email", "placeholder":"E-poçt:"}))


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(label='Yeni şifrə', widget=forms.PasswordInput(attrs={"placeholder": "Yeni şifrə:", "class": "form-control"}))
    password2 = forms.CharField(label='Təkrar şifrə', widget=forms.PasswordInput(attrs={"placeholder": "Təkrar yeni şifrə:", "class": "form-control"}))

    def clean(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not (password1 and password2 and password1 == password2):
            raise forms.ValidationError("Şifrələr uyğun deyil")

        if len(password1) < 8:
            raise forms.ValidationError("Şifrənin uzunluğu minimum 8 simvoldan ibarət olmalıdır.")