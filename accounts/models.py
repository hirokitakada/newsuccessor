
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
    """
    Create and save user with email
    """
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Django標準のUserをベースにカスタマイズしたUserクラス
    """
    username_validator = UnicodeUsernameValidator()
    # python3で半角英数のみ許容する場合はASCIIUsernameValidatorを用いる
    # username_validator = ASCIIUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=50,
        unique=False,
        blank=False,
        # help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        help_text='この項目は必須です。全角文字、半角英数字、@/./+/-/_ で50文字以下にしてください。',
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    # first_name = models.CharField(_('first name'), max_length=30, blank=True)
    # last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(
        _('email address'),
        help_text='この項目は必須です。メールアドレスは公開されません。',
        blank=False,
        unique = True
    )


    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    profile = models.ImageField(upload_to='profile/',blank=True)
    picture = models.ImageField(upload_to='picture/',blank=True)
    text = models.TextField(max_length=200,blank=True)

    startyear = models.IntegerField(default=2020,blank=True)
    company = models.CharField(max_length=200,blank=True)
    department = models.CharField(max_length=200,blank=True)
    section = models.CharField(max_length=200,blank=True)
    first_period = models.DateField(default=timezone.now,blank=True)
    end_period = models.DateField(default=timezone.now,blank=True)
    enrolment = models.BooleanField(default=True,blank=True)
    hobby = models.CharField(max_length=200,blank=True)
    activities_1 = models.CharField(max_length=200,blank=True)
    activities_2 = models.CharField(max_length=200,blank=True)
    other = models.CharField(max_length=200,blank=True)
    message = models.CharField(max_length=200,blank=True)


    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # abstract = True
        abstract = False

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    # first_nameとlast_nameに関する部分はコメントアウト
    # def get_full_name(self):
    #     """
    #     Return the first_name plus the last_name, with a space in between.
    #     """
    #     full_name = '%s %s' % (self.first_name, self.last_name)
    #     return full_name.strip()

    # def get_short_name(self):
    #     """Return the short name for the user."""
    #     return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)



class Image(models.Model):
    picture = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title