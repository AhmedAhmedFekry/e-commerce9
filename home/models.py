from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, TextInput, Textarea
from django.utils.safestring import mark_safe
# Create your models here.
class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=15)
    fax = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=True, max_length=50)
    smtpserver = models.CharField(blank=True, max_length=50)
    smtpemail = models.CharField(blank=True, max_length=50)
    smtppassword = models.CharField(blank=True, max_length=10)
    smtpport = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    
class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(blank=True, max_length=20, verbose_name=_('name'))
    email = models.CharField(blank=True, max_length=50,
                             verbose_name=_('email'))
    subject = models.CharField(
        blank=True, max_length=50, verbose_name=_('subject'))
    message = models.TextField(
        blank=True, max_length=255, verbose_name=_('message'))
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = [_('name'), _('email'), _('subject'), _('message')]
        widgets = {
            _('name'): TextInput(attrs={'class': 'input', 'placeholder': _('Name & Surname')}),
            _('subject'): TextInput(attrs={'class': 'input', 'placeholder': _('Subject')}),
            _('email'): TextInput(attrs={'class': 'input', 'placeholder': _('Email Address')}),
            _('message'): Textarea(attrs={'class': 'input', 'style': 'height:100px', 'placeholder': _('Your Message'), 'rows': '100'}),
        }
class Offer(models.Model):
    name= models.CharField(_("name"), max_length=50)
    link=models.URLField(_("link"), max_length=200)
    image=models.ImageField(_("image"), upload_to='images/offer/')
    description= RichTextUploadingField(blank=True)
    def __str__(self):
        return self.name
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="80"/>'.format(self.image.url))
        else:
            return ""


class FAQ(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
