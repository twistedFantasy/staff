from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from ssm.core.models import BaseModel


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseModel):
    email = models.EmailField('Email', unique=True, max_length=256)
    is_active = models.BooleanField('Is Active', default=True)
    is_staff = models.BooleanField('Is Staff', default=False, db_index=True)
    is_superuser = models.BooleanField('Is Superuser', default=False, db_index=True)

    # metadata
    full_name = models.CharField('Full Name', max_length=256, default='', blank=True)
    ld_number = models.IntegerField('L/D Number', null=True, blank=True)
    position = models.CharField('Position', max_length=68, null=True, blank=True)
    date_of_birth = models.DateField('Date of Birth', null=True, blank=True)
    hired_date = models.DateField('Hired Date', null=True, blank=True)
    end_of_contract = models.DateField('End of Contract', null=True, blank=True)
    education = models.CharField('Education', max_length=32, null=True, blank=True)
    phone_number = models.CharField('Phone Number', max_length=32, null=True, blank=True)
    phone_number2 = models.CharField('Phone Number 2', max_length=32, null=True, blank=True)
    has_card = models.BooleanField('Has Card', default=False)
    has_key = models.BooleanField('Has Key', default=False)
    skype = models.CharField('Skype', max_length=32, null=True, blank=True)
    working_hours = models.IntegerField('Working Hours', default=8)
    skills = models.ManyToManyField('Skill', through='UserSkillModel')

    # assessment
    assessment_date = models.DateField('Assessment Date', null=True, blank=True)
    assessment_plan = models.TextField('Assessment Plan', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'users'
        ordering = ['-modified']
        verbose_name_plural = 'Users'

    def __str__(self):
        return u'%s (user %s)' % (self.get_full_name(), self.id)

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
