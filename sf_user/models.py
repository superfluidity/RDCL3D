from __future__ import unicode_literals

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.sessions.base_session import AbstractBaseSession
from django.db import models

class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser."""

    def _create_user(self, username, password, is_staff, is_superuser, **extra_fields):
        """Create and save a CustomUser with the given username and password. """
        now = timezone.now()

        if not username:
            raise ValueError('The given username must be set')

        is_active = extra_fields.pop("is_active", True)
        user = self.model(username=username, is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    """Create and save an CustomUser with the given username and password."""
    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True, is_admin=True,
                                 **extra_fields)

    """Create and save an FullOperator with the given email and password. """
    def create_full_operator(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, False, is_full_operator=True,
                                 **extra_fields)

    """Create and save an BasicUser with the given email and password. """
    def create_basic_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, False, is_basic_user=True,
                                 **extra_fields)

    """Create and save an GuestUser with the given email and password. """
    def create_guest_user(self, username, password="guest", **extra_fields):
        return self._create_user(username, password, False, False, is_guest_user=True,
                                 **extra_fields)


class AbstractCustomUser(AbstractBaseUser, PermissionsMixin):
    """Abstract User with the same behaviour as Django's default User.

    AbstractCustomUser does not have username field. Uses email as the
    USERNAME_FIELD for authentication.

    Use this if you need to extend EmailUser.

    Inherits from both the AbstractBaseUser and PermissionMixin.

    The following attributes are inherited from the superclasses:
        * password
        * last_login
        * is_superuser

    """
    username = models.CharField(_('username'), max_length=255, unique=True, db_index=True)

    email = models.EmailField(_('email address'), max_length=255, unique=True)

    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    phone = models.CharField(_('phone'), max_length=100, blank=True)
    # user_groups = models.ManyToManyField(UserGroup, verbose_name=_('user groups'), blank=True)

    is_admin = models.BooleanField(_('admin status'), default=False)
    is_full_operator = models.BooleanField(_('full_operator status'), default=False)
    is_basic_user = models.BooleanField(_('basic_user status'), default=False)
    is_guest_user = models.BooleanField(_('guest_user status'), default=False)

    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_(
            'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as '
        'active. Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone', ]

    class Meta:
        verbose_name = _('custom user')
        verbose_name_plural = _('custom users')
        abstract = True

    def get_full_name(self):
        """Return the fullname."""
        return "%s %s" % (self.last_name, self.first_name)

    def get_short_name(self):
        """Return the firstname."""
        return self.first_name


class CustomUser(AbstractCustomUser):
    """
    Concrete class of AbstractCustomUser.

    Use this if you don't need to extend CustomUser.

    """

    class Meta(AbstractCustomUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def count_admins(self):
        return CustomUser.objects.filter(is_admin=True).count()

    def count_employee(self):
        return CustomUser.objects.filter(is_full_operator=True).count()

    def count_basic_users(self):
        return CustomUser.objects.filter(is_basic_user=True).count()

    def count_inactives(self):
        return CustomUser.objects.filter(is_active=False).count()

    def is_guest(self):
        return self.is_guest_user

    def get_avatar(self):
        if self.is_admin:
            return "assets/img/employer.jpg"
        elif self.is_full_operator:
            return "assets/img/employer.jpg"
        elif self.is_basic_user:
            return "assets/img/employer.jpg"
        elif self.is_guest_user:
            return "assets/img/punto.png"

    def get_user_role(self):
        if self.is_admin:
            return 0, "Admin"
        elif self.is_full_operator:
            return 1, "Full operator"
        elif self.is_basic_user:
            return 2, "Basic user"
        elif self.is_guest_user:
            return 3, "Guest user"

    def get_user_role_name(self):
        if self.is_admin:
            return "Admin"
        elif self.is_full_operator:
            return "Full operator"
        elif self.is_basic_user:
            return "Basic user"
        elif self.is_guest_user:
            return "Guest user"

class CustomSession(AbstractBaseSession):
    account_id = models.IntegerField(null=True, db_index=True)

    @classmethod
    def get_session_store_class(cls):
        return SessionStore

