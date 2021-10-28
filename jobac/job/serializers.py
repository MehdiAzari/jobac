from django.db.models import fields
from rest_framework import serializers
from rest_framework.utils.field_mapping import needs_label

from .models import JobOffer, Proposal
from User.serializers import EmployerSerializer, FreelancerSerializer


class JobOfferSerializer(serializers.ModelSerializer):
    jobOffer = serializers.SerializerMethodField()

    class Meta:
        model = JobOffer
        fields = ('id', 'title', 'employer', 'deadline', 'fee', 'needed_skills', 'image', 'hours')

    def get_employer(self, obj):
        e = EmployerSerializer(obj.employer).data
        e.pop('user')
        return e

    def create(self, validated_data):
        jobOffer = JobOffer.objects.update_or_create(
            employer=self.context['request'].user.employer, title=validated_data.get('title'),
            deadline=validated_data.get['deadline'],
            fee=validated_data.get('deadline'),
            needs_skills=validated_data.get('needed_skills'),
            image=validated_data.get('image'),
            hours=validated_data.get('image'))
        return jobOffer


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = ('proposal', 'bid', 'is_accepted')


class ProposalListSerializer:
    """
    using this serializer for listing proposal related to 
    specific job to the owner of job.
    """
    
    freelancer = serializers.SerializerMethodField(read_only=True)
    job = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Proposal
        fields = ('proposal','freelancer')
        
    def get_freelancer(self,obj):
        o = FreelancerSerializer(obj.freelancer).data
        o.pop('user')
        return o
    def get_job_offer(self,obj):
        j = JobOfferSerializer(obj.job).data
        j.pop('employer')
        return j
