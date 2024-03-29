from rest_framework import viewsets, generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
import datetime
from rest_framework.filters import SearchFilter
from recruiter.models import Recruiter
from student.models import StudentApplication
from student.models import StudentNotification
from student.models import Student

from intershala_admin.models import IntershalaCompany


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileReadSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ('profile_name', 'experience', 'employment_type', 'schedule', 'location', 'recruiter__company')
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            Profile.applied_application_counter(self=self)
            Profile.selected_application_counter(self=self)
            Profile.rejected_application_counter(self=self)
            Profile.intouch_application_counter(self=self)
            Profile.total_application_counter(self=self)
            query = Profile.objects.filter(recruiter=Recruiter.objects.get(user=self.request.user.id)).order_by(
                '-created_at')
            query = self.filter_queryset(self.get_queryset())
            serializer = ProfileReadSerializer(query, many=True)
            return Response(serializer.data)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def create(self, request, *args, **kwargs):
        try:
            if self.request.user.is_recruiter:
                recruiter_query = Recruiter.objects.get(user=self.request.user.id)
                if recruiter_query.active:
                    serializer = ProfileSerializer(data=self.request.data)
                    if serializer.is_valid(raise_exception=True):
                        data = serializer.save(recruiter=recruiter_query, active=True,
                                               company=IntershalaCompany.objects.get(id=recruiter_query.company.id))
                        recruiter_query = Recruiter.objects.get(user=self.request.user.id)
                        recruiter_query.created_profile.add(data)
                        return Response(serializer.data, status=200)
                    else:
                        return Response(serializer.errors, status=401)
                elif not recruiter_query.active:
                    return Response({"NO_ACCESS": "Access Denied"}, status=401)
        except:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def update(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            try:
                instance = Profile.objects.get(id=self.kwargs["id"],
                                               recruiter=Recruiter.objects.get(user=self.request.user.id))
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            print(instance, 'check here')
            serializer = ProfileSerializer(instance, data=self.request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                recruiter_query = Recruiter.objects.get(user=self.request.user.id)
                if recruiter_query.active:
                    serializer.save(updated_at=datetime.datetime.now())
                elif not recruiter_query.active:
                    return Response({"NO_ACCESS": "Access Denied"}, status=401)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=401)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            try:
                instance = Profile.objects.get(id=self.kwargs["id"],
                                               recruiter=Recruiter.objects.get(user=self.request.user.id))
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            recruiter_query = Recruiter.objects.get(user=self.request.user.id)
            if recruiter_query.active:
                instance.delete()
            elif not recruiter_query.active:
                return Response({"NO_ACCESS": "Access Denied"}, status=401)
            return Response({"Profile Deleted": "Access Granted"}, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def retrieve(self, request, *args, **kwargs):
        global serializer
        if self.request.user.is_recruiter:
            try:
                instance = Profile.objects.get(id=self.kwargs["id"],
                                               recruiter=Recruiter.objects.get(user=self.request.user.id))
                recruiter_query = Recruiter.objects.get(user=self.request.user.id)
                if recruiter_query.active:
                    serializer = self.get_serializer(instance)
                elif not recruiter_query.active:
                    return Response({"NO_ACCESS": "Access Denied"}, status=401)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class StudentApplicationsViewSet(generics.RetrieveUpdateAPIView):
    queryset = StudentApplication.objects.all()
    serializer_class = StudentApplicationReadSerializer
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            query = StudentApplication.objects.get(id=self.kwargs["id"])
            serializer = self.get_serializer(query)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def update(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            try:
                instance = StudentApplication.objects.get(id=self.kwargs["id"])
                student_query = Student.objects.get(id=instance.student.id)
                profile_query = Profile.objects.get(id=instance.profile.id)
                company_query = IntershalaCompany.objects.get(id=profile_query.company.id)
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            serializer = self.get_serializer(instance, data=self.request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                data = serializer.save(updated_at=datetime.datetime.now())
                if data.status == "Selected":
                    StudentNotification.selected(student=student_query, student_name=student_query.first_name,
                                                 profile_name=profile_query.profile_name,
                                                 company_name=company_query.company_name, self=self)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=401)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class AssessmentQuestionViewsets(generics.ListAPIView):
    queryset = Assessment_question.objects.all().order_by('-created_at')
    serializer_class = AssessmentReadQuestionSerializer
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            query = Assessment_question.objects.filter(
                recruiter=Recruiter.objects.get(user=self.request.user.id)).order_by(
                '-created_at')
            serializer = self.get_serializer(query, many=True)
            return Response(serializer.data)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class AssessmentQuestionCreateViewsets(generics.CreateAPIView):
    queryset = Assessment_question.objects.all().order_by('-created_at')
    serializer_class = AssessmentWriteQuestionSerializer
    lookup_field = "id"

    def perform_create(self, serializer):
        try:
            if self.request.user.is_recruiter:
                serializer = AssessmentWriteQuestionSerializer(data=self.request.data)
                if serializer.is_valid(raise_exception=True):
                    data = serializer.save(recruiter=Recruiter.objects.get(user=self.request.user.id), active=True)
                    profile_query = Profile.objects.get(id=self.request.data.get('profile'))
                    profile_query.question.add(data)
                    return Response(serializer.data, status=200)
                else:
                    return Response(serializer.errors, status=401)
        except:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def update(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            try:
                instance = Assessment_question.objects.get(id=self.kwargs["id"],
                                                           recruiter=Recruiter.objects.get(user=self.request.user.id))
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            serializer = AssessmentWriteQuestionSerializer(instance, data=self.request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(updated_at=datetime.datetime.now())
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=401)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            try:
                instance = Assessment_question.objects.get(id=self.kwargs["id"],
                                                           recruiter=Recruiter.objects.get(user=self.request.user.id))
                profile_query = Profile.objects.get(id=instance.profile.id)
                profile_query.question.remove(instance)
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            instance.delete()
            return Response({"Question Deleted": "Access Granted"}, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            try:
                instance = Assessment_question.objects.get(id=self.kwargs["id"],
                                                           recruiter=Recruiter.objects.get(user=self.request.user.id))
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
