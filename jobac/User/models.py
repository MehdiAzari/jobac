
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator
from datetime import date
from django.db.models.enums import IntegerChoices
from django.utils.translation import gettext as _
# Create your models here.


class Skills(models.Model):
    '''
    Skills that freelancers work on

    '''
    skills = (
        ('SOFTWARE_ENGINEER', 'SOFTWARE_ENGINEER'),
        ('UI_DESIGNER', 'UI_DESIGNER'),
        ('DATA_SCIENTIST', 'DATA_SCIENTIST'),
        ('CLOUD_ENGINEER', 'CLOUD_ENGINEER'),
        ('DevOps_ENGINEER', 'DevOps_ENGINEER'),
        ('UX_DESIGNER', 'UX_DESIGNER'),
        ('WEB_DEVELOPER', 'WEB_DEVELOPER'))

    name = models.CharField(max_length=65, choices=skills, blank=False, null=False)


class Document(models.Model):
    """
    this class is the model of resume.
    holds it's properties and connect it to freelancers
    """
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/', blank=True,
                                validators=[FileExtensionValidator(['pdf'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    '''
    base User class, used for authentications
    in our rest framework
    @user_groups determines tyoe of user
    '''
    class AuthType(models.IntegerChoices):
        ADMIN = 1
        EMPOYER = 2
        FREELANCER = 3

    # type of user
    user_group = models.IntegerField(
        choices=AuthType.choices, default=1, blank=False, null=False)

    def __str__(self):
        return self.AuthType


class Freelancer(models.Model):
    """
    This class represents karjoo
    resume is related to the Document where user
    uploads his/her resume. We use foreignKey for connecting
    it to database and make a relation between files and freelancers
    """
    class Sex(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        UNKOWN = 'U', _('Uknown')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=63, null=False, blank=False)
    family_name = models.CharField(max_length=63, null=False, blank=False)
    sex = models.TextField(choices=Sex.choices,
                           default='u', blank=False, null=False)
    age = models.PositiveIntegerField(null=False, blank=False,)
    skills = models.ManyToManyField(Skills, blank=True, null=True)
    resume = models.ForeignKey(Document, on_delete=models.CASCADE)


class Employer(models.Model):
    """
    This class represents karfarma
    fields is related to skills that company is looking for
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=False, null=False)
    fields = models.ManyToManyField(Skills, blank=True, null=True)
    number = models.CharField(max_length=11, blank=False, null=False)
    foundation_year = models.PositiveSmallIntegerField(
        blank=False, null=False,)
