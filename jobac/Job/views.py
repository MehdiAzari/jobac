from django.utils import timezone
import sys
from django.shortcuts import render
from rest_framework import status
from rest_framework import filters
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (AllowAny, IsAuthenticated)

from Job.permissions import IsOwner
from jobac.User.models import Freelancer
from jobac.User.permissions import IsNotBlackListed, isEmployer
from .models import JobOffer, Proposal
from .serializers import JobOfferSerializer, ProposalSerializer, ProposalListSerializer


class Node:
    def __init__(self, key, pk):
        self.right = None
        self.left = None
        self.pk = pk
        self.val = key


def arrayToBinarySearchTree(array):
    """
        takes a sorted array as an argument and returns an array
        in preorder traversal of constructed BST
    """
    if not array:
        return None

    size = int(len(array))
    mid = size / 2
    root = array[mid]

    root.right = arrayToBinarySearchTree(array[mid + 1:])
    root.left = arrayToBinarySearchTree(array[:mid])
    return root


def RangeFilter(minRange, maxRange, root):
    """
        We could use // Sample.objects.filter(date__range=[startdate, enddate])
        but we don't have access to database for this as customer explained in the
        doc we put all the data in BST and use range filter algorithm
    """
    ans = []

    def recursion(minimum, maximum, tmproot):
        if tmproot is None:
            return
        if tmproot.val < minimum:
            recursion(minimum, maximum, tmproot.right)

        if minimum <= tmproot.val <= maximum:
            ans.append(tmproot.pk)
            recursion(minimum, maximum, tmproot.left)
            recursion(minimum, maximum, tmproot.right)

        if tmproot.val > maximum:
            recursion(minimum, maximum, tmproot.left)
        return

    recursion(minRange, maxRange, root)
    return ans


class FeeRangeFilter(filters.BaseFilterBackend):
    """
    sorting jobs by fee
    """

    def filter_queryset(self, request, _, __):
        min_fee = request.query_params.get("min_fee", 0)
        max_fee = request.query_params.get(
            "max_fee", sys.maxsize)
        jobOffers = JobOffer.objects.all()
        arr = []
        for jobOffer in jobOffers:
            node = Node(jobOffer.fee, jobOffer.pk)
            arr.append(node)
        arr = sorted(arr, key=lambda nd: nd.val)
        root = arrayToBinarySearchTree(arr)
        pks = RangeFilter(int(min_fee), int(max_fee), root)
        qs = jobOffer.objects.filter(pk__in=pks)
        return qs


class JobOfferList(generics.ListAPIView):
    """
    This View shows list of available jobs
    """

    def get_queryset(self):
        return JobOffer.objects.all()

    serializer_class = JobOfferSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter,
                       filters.SearchFilter, FeeRangeFilter]
    ordering_fields = ['fee', 'deadline', 'hours', 'needed_skills']
    search_fields = ['title']


class JobOfferCreate(generics.CreateAPIView):
    queryset = JobOffer.objects.all()
    permission_classes = [IsAuthenticated, isEmployer, IsNotBlackListed]
    serializer_class = JobOfferSerializer

    def post(self, request, *args, **kwargs):
        """
        Creating job offer by post HTTP method
        sends 201 if succeeded
        sends 400 if sth went wrong
        """
        serializer = JobOfferSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class JobOfferUpdate(generics.RetrieveUpdateAPIView):
    queryset = JobOffer.objects.all()
    permission_classes = [IsAuthenticated, IsOwner, IsNotBlackListed]
    serializer_class = JobOfferSerializer


class JobOfferDetail(generics.RetrieveAPIView):
    queryset = JobOffer.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = JobOfferSerializer


class JobOfferDelete(generics.RetrieveDestroyAPIView):
    queryset = JobOffer.objects.all()
    permission_classes = [IsAuthenticated, IsOwner, IsNotBlackListed]
    serializer_class = JobOfferSerializer


class SubmitProposal(generics.CreateAPIView):
    queryset = Proposal.objects.all()
    permission_classes = [IsAuthenticated, Freelancer, IsNotBlackListed]
    serializer_class = ProposalSerializer

    def post(self, request, *args, **kwargs):
        jobOffer = JobOffer.objects.get(pk=request.data['JobOffer'])
        if timezone.now() < JobOffer.deadline:
            submit, _ = Proposal.objects.get_or_create(
                person=request.user.freelancer, JobOffer=jobOffer)
            submit.save()
            return Response("Your Proposal is sent", status=status.HTTP_200_OK)
        return Response("JobOffer expired", status=status.HTTP_400_BAD_REQUEST)


class ListEmployersProposals(generics.ListAPIView):
    """
    this View is lists proposal of freelancers for employer's job.
    only the owner of posted job has access to this list
    """
    permission_classes = [IsAuthenticated, isEmployer]
    serializer_class = ProposalListSerializer

    def get_queryset(self):
        return Proposal.objects.filter(job__employer=self.request.user.employer)
