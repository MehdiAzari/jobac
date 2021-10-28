from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator
from datetime import date
# Create your models here.


class Skills(models.IntegerChoices):
    '''
    Skills that freelancers work on
    '''
    SOFTWARE_ENGINEER = 1
    CLOUD_ENGINEER = 2
    DevOps_ENGINEER = 3
    WEB_DEVELOPER = 4
    UX_DESIGNER = 5
    UI_DESIGNER = 6
    DATA_SCIENTIST = 7


class User(AbstractUser):
    '''
    base User class, used for authentications
    in our rest framework

    '''
    class AuthType(models.IntegerChoices):
        ADMIN = 1
        EMPOYER = 2
        FREELANCER = 3

    # type of user
    user_type = models.IntegerField(
        choices=AuthType.choices, default=1, blank=False, null=False)

    def __str__(self):
        return self.AuthType


class Document(models.Model):
    """
    this class is the model of resume.
    holds it's properties and connect it to freelancers
    """
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/', blank=True,
                                validators=[FileExtensionValidator(['pdf'])])
    uploaded_at = models.DateTimeField(auto_now_add=True,validators=)


class Freelancer(models.Model):
    """
    This class represents کارجو
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
    This class represents کارفرما
    fields is related to skills that company is looking for
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=False, null=False)
    fields = models.ManyToManyField(Skills, blank=True, null=True)
    number = models.CharField(max_length=11, blank=False, null=False)
    foundation_year = models.PositiveSmallIntegerField(
        max_length=4, blank=False, null=False, validators=MaxValueValidator(date.today().year, "invalid year"),)
