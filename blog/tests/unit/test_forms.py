from django.test import TestCase
from unittest import skip
from blog.forms import SigninForm, LoginForm
from django import forms

class TestLoginForm(TestCase):
    def setUp(self) -> None:
        self.form = LoginForm()
        
    def test_if_login_form_testcase_is_running(self) -> None:
        self.assertTrue(True)
        
    def test_if_login_form_class_exists(self) -> None:
        from blog.forms import LoginForm
        
    def test_if_login_form_is_a_django_form(self) -> None:
        form = LoginForm()
        self.assertIsInstance(form, forms.Form)
        
    def test_if_login_form_has_fields(self) -> None:
        self.assertTrue(self.form.fields)

    def test_if_login_form_has_email_field(self) -> None:
        self.assertIn('email', self.form.fields)
        
    def test_if_email_field_is_required(self) -> None:
        self.assertTrue(self.form.fields["email"].required)
        
    def test_if_email_field_is_emailfield(self) -> None:
        self.assertIsInstance(self.form.fields["email"], forms.EmailField)
 
    def test_if_email_field_have_label(self) -> None:
        self.assertFalse(self.form.fields["email"].label is None)
    
    def test_email_field_label_content(self) -> None:
        self.assertEqual(self.form.fields["email"].label, "Email")
 
    def test_if_login_form_has_password_field(self) -> None:
        self.assertIn('password', self.form.fields)

    def test_if_login_form_password_field_is_charfield(self) -> None:
        self.assertIsInstance(self.form.fields["password"], forms.CharField)
        
    def test_if_login_form_password_field_is_required(self) -> None:
        self.assertTrue(self.form.fields["password"].required)
        
    def test_if_login_form_password_field_have_password_input_widget(self) -> None:
        self.assertIsInstance(self.form.fields["password"].widget, forms.PasswordInput)
        
    def test_if_login_form_hve_password_label(self) -> None:
        self.assertFalse(self.form.fields["password"].label is None)
        
    def test_login_form_password_field_content(self) -> None:
        self.assertEqual(self.form.fields["password"].label, "Password")
 
 
 
class TestSigninForm(TestCase):
    def setUp(self) -> None:
        self.form = SigninForm()
    
    def test_if_signin_form_testcase_is_running(self) -> None:
        self.assertTrue(True)
        
    def test_if_signin_form_class_exists(self) -> None:
        from blog.forms import SigninForm 
        
    def test_if_signin_form_is_a_django_form(self) -> None:
        self.assertIsInstance(self.form, forms.Form)
        
    def test_if_signin_form_has_fields(self) -> None:
        self.assertTrue(self.form.fields)
        
    def test_if_signin_form_has_first_name_field(self) -> None:
        self.assertIn('first_name', self.form.fields)
        
    def test_if_signin_form_has_last_name_field(self) -> None:
        self.assertIn('last_name', self.form.fields)
        
    def test_if_signin_form_has_password_field(self) -> None:
        self.assertIn('password', self.form.fields)
        
    def test_if_signin_form_fields_are_charfields(self) -> None:
        self.assertIsInstance(self.form.fields['first_name'], forms.CharField)
        self.assertIsInstance(self.form.fields['last_name'], forms.CharField)
        self.assertIsInstance(self.form.fields['password'], forms.CharField)
        
    def test_first_name_field_is_required(self) -> None:
        self.assertTrue(self.form.fields["first_name"].required)    
        
    def test_if_last_name_field_is_not_required(self) -> None:
        self.assertFalse(self.form.fields["last_name"].required)
        
    def test_if_password_form_field_is_required(self) -> None:
        self.assertTrue(self.form.fields["password"].required)
        

    def test_password_field_is_password_widget(self) -> None: 
        self.assertIsInstance(self.form.fields["password"].widget, forms.PasswordInput)
        
    def test_first_name_field_have_label(self) -> None:
        self.assertIsNotNone(self.form.fields["first_name"].label)
        
    def test_first_name_field_label_content(self) -> None:
        self.assertEqual(self.form.fields["first_name"].label, "Type your first name")    
    
    def test_password_field_have_label(self) -> None:
        self.assertIsNotNone(self.form.fields["password"].label)
        
    def test_password_field_label_content(self) -> None:
        self.assertEqual(self.form.fields["password"].label, "Type your password")
        
    def test_signin_form_valid_with_data(self) -> None:
        form = SigninForm(data={
            "first_name": "John",
            "last_name": "Doe",
            "email":"teste.teste@email.com",
            "password": "strongPassword123"
        })
        self.assertTrue(form.is_valid())            
        
    def test_signin_form_validate_with_wrong_types(self) -> None:
        form = SigninForm(data={
            "first_name": 123,
            "last_name": True,
            "email":"asdsad",
            "password": ["array"]
        })
        self.assertFalse(form.is_valid())
            
    def test_singin_form_last_name_input_has_label(self) -> None:
        self.assertEqual(self.form.fields["last_name"].label, "Type your last name")
        
    def test_singin_form_have_email_field(self) -> None:
        self.assertIn('email', self.form.fields)
        
    def test_signin_form_email_field_is_emailfield(self) -> None:
        self.assertIsInstance(self.form.fields["email"], forms.EmailField)
        
    def test_signin_form_email_field_is_required_and_have_label(self) -> None:
        self.assertTrue(self.form.fields["email"].required)
        self.assertIsNotNone(self.form.fields["email"].label)
        self.assertEqual(self.form.fields["email"].label, "Type your email")

    @skip("Not implemented yet")
    def test_if_form_validate_with_same_password_input(self) -> None:
        pass

    @skip("Not implemented yet")
    def test_if_form_raises_error_with_different_password_input(self) -> None:
        pass