from django.db import models
from User.models import Freelancer, Employer, Skills
# Create your models here.


class JobOffer(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    fee = models.IntegerField(default=0, blank=False, null=False)
    hours = models.IntegerField(blank=False, null=False)
    needed_skills = models.ManyToManyField(Skills, blank=True)
    deadline = models.DateField()
    image = models.ImageField(upload_to='offers/images/')

    def __str__(self):
        return self.title + " from " + self.employer.name


class Proposal(models.Model):
    """
    Sent offers from freelancers
    they are related to job
    we need to hold it to track freelancer's offers
    """
    job = models.ForeignKey(JobOffer, on_delete=models.DO_NOTHING)
    bid = models.FloatField(blank=False, null=False)
    is_accepted = models.BooleanField(blank=False, null=False)
    freelancer = models.ForeignKey(Freelancer, models.CASCADE)
