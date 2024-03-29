from datetime import datetime
from user.models import User
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from student.models import Student
from job_profile.models import Profile, Skill
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.filters import SearchFilter
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from student.models import StudentNotification
from Django_Intershala.settings import EMAIL_HOST_USER


class IntershalaAdminListView(generics.ListAPIView, generics.CreateAPIView):
    queryset = IntershalaAdmin.objects.all()
    serializer_class = IntershalaAdminSerializer

    def list(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            queryset = IntershalaAdmin.objects.all().order_by('-created_at')
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            serializer = self.get_serializer(data=self.request.data)
            user_query = User.objects.get(id=self.request.data.get('user'))
            user_query.is_admin = True
            user_query.save()
            try:
                qrcode_img = qrcode.make(self.request.data['first_name'] + " intershala_admin")
                canvas = Image.new('RGB', (290, 290), 'white')
                draw = ImageDraw.Draw(canvas)
                canvas.paste(qrcode_img)
                username = self.request.data['first_name']
                fname = f'intershala_code-{username}' + '.png'
                buffer = BytesIO()
                canvas.save(buffer, 'PNG')
                user_query.qr_code.save(fname, File(buffer), save=True)
                canvas.close()
            except:
                pass
            if serializer.is_valid(raise_exception=True):
                data = serializer.save(first_name=user_query.first_name, last_name=user_query.last_name,
                                       email=user_query.email, active=True)
                AdminNotification.admin_added(admin_name=user_query.first_name, admin=data)
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=401)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class IntershalaAdminUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IntershalaAdmin.objects.all()
    serializer_class = IntershalaAdminSerializer
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            try:
                instance = IntershalaAdmin.objects.get(id=self.kwargs["id"])
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def update(self, request, *args, **kwargs):
        try:
            if self.request.user.is_superuser:
                try:
                    queryset = IntershalaAdmin.objects.get(id=self.kwargs["id"])
                except ObjectDoesNotExist:
                    return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
                serializer = self.get_serializer(queryset, data=self.request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    if serializer.validated_data.get('active'):
                        user_query = User.objects.get(id=request.data.get('user'))
                        AdminNotification.admin_added(admin_name=user_query.first_name, admin=queryset)
                        user_query.is_admin = True
                        user_query.save()
                        serializer.save(updated_at=datetime.now(), active=True)
                    elif not serializer.validated_data.get('active'):
                        user_query = User.objects.get(id=request.data.get('user'))
                        AdminNotification.admin_removed(admin_name=user_query.first_name, admin=queryset)
                        user_query.is_admin = False
                        user_query.save()
                        serializer.save(updated_at=datetime.now(), active=False)
                    return Response(serializer.data, status=200)
                else:
                    return Response(serializer.errors, status=400)
        except:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            try:
                instance = IntershalaAdmin.objects.get(id=self.kwargs["id"])
                user_query = User.objects.get(id=instance.user.id)
                AdminNotification.admin_removed(admin_name=user_query.first_name)
                user_query.is_admin = False
                user_query.save()
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            instance.delete()
            return Response({"Admin Deleted": "Access Granted"}, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class IntershalaStudentViewSets(generics.ListAPIView):
    queryset = Student.objects.all().order_by('-created_at')
    serializer_class = IntershalaStudentSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [SearchFilter, ]
    search_fields = ['first_name', 'email']

    def list(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin:
            queryset = self.get_queryset()
            queryset = self.filter_queryset(queryset)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class IntershalaStudentUpdateViewSets(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all().order_by('-created_at')
    serializer_class = IntershalaStudentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_admin or self.request.user.is_employee or self.request.user.is_superuser:
            try:
                queryset = Student.objects.get(id=self.kwargs["id"])
                serializer = self.get_serializer(queryset)
                return Response(serializer.data, status=200)
            except:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def update(self, request, *args, **kwargs):
        try:
            if self.request.user.is_admin or self.request.user.is_employee or self.request.user.is_superuser:
                try:
                    queryset = Student.objects.get(id=self.kwargs["id"])
                    serializer = self.get_serializer(queryset, data=self.request.data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        if serializer.validated_data.get('active'):
                            StudentNotification.updated_student(self=self, student=queryset,
                                                                student_name=queryset.first_name,
                                                                from_email=EMAIL_HOST_USER, email=queryset.email)
                            user_query = User.objects.get(id=queryset.user.id)
                            user_query.is_student = True
                            user_query.save()
                            serializer.save(updated_at=datetime.now(), active=True)
                        elif not serializer.validated_data.get('active'):
                            StudentNotification.removed_student(self=self, student=queryset,
                                                                student_name=queryset.first_name,
                                                                from_email=EMAIL_HOST_USER, email=queryset.email)
                            user_query = User.objects.get(id=queryset.user.id)
                            user_query.is_student = False
                            user_query.save()
                            serializer.save(updated_at=datetime.now(), active=False)
                        return Response(serializer.data, status=200)
                    else:
                        return Response(serializer.errors, status=400)
                except ObjectDoesNotExist:
                    return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
        except:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin:
            try:
                instance = self.queryset.get(id=self.kwargs["id"])
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            instance.active = False
            instance.save()
            StudentNotification.removed_student(self=self, student=instance,
                                                student_name=instance.first_name, from_email=EMAIL_HOST_USER,
                                                email=instance.email)
            user_query = User.objects.get(id=instance.user.id)
            user_query.is_student = False
            user_query.save()
            return Response({"Student Deleted": "Access Granted"}, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class IntershalaJobProfileViewSets(generics.ListAPIView, generics.DestroyAPIView, generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all().order_by('-created_at')
    serializer_class = IntershalaJobProfileReadSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    filter_backends = [SearchFilter, ]
    search_fields = ['profile_name', 'skills__skill_name', 'active']

    def list(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin:
            queryset = self.get_queryset()
            queryset = self.filter_queryset(queryset)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_admin or self.request.user.is_employee or self.request.user.is_customer:
            try:
                queryset = Profile.objects.get(id=self.kwargs["id"])
                serializer = IntershalaJobProfileReadSerializer(queryset)
                return Response(serializer.data, status=200)
            except:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def update(self, request, *args, **kwargs):
        try:
            if self.request.user.is_admin or self.request.user.is_employee:
                try:
                    queryset = Profile.objects.get(id=self.kwargs["id"])
                    serializer = self.get_serializer(queryset, data=self.request.data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save(updated_at=datetime.now())
                        return Response(serializer.data, status=200)
                    else:
                        return Response(serializer.errors, status=400)
                except ObjectDoesNotExist:
                    return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
        except:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin:
            try:
                instance = self.queryset.get(id=self.kwargs["id"])
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            instance.delete()
            return Response({"Recruiter Deleted": "Access Granted"}, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class IntershalaSkillViewSets(generics.ListCreateAPIView):
    queryset = Skill.objects.all().order_by('-created_at')
    serializer_class = IntershalaSkillReadSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [SearchFilter, ]
    search_fields = ['skill_name', 'active']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def create(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin or self.request.user.is_recruiter:
            serializer = IntershalaWriteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=self.request.user, active=True)
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class IntershalaSkillUpdateViewSets(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all().order_by('-created_at')
    serializer_class = IntershalaSkillReadSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_admin or self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_recruiter:
            try:
                queryset = Skill.objects.get(id=self.kwargs["id"])
                serializer = self.get_serializer(queryset)
                return Response(serializer.data, status=200)
            except:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def update(self, request, *args, **kwargs):
        try:
            if self.request.user.is_admin or self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_recruiter:
                try:
                    queryset = Skill.objects.get(id=self.kwargs["id"])
                    serializer = IntershalaWriteSerializer(queryset, data=self.request.data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save(updated_at=datetime.now())
                        return Response(serializer.data, status=200)
                    else:
                        return Response(serializer.errors, status=400)
                except ObjectDoesNotExist:
                    return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
        except:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_employee or self.request.user.is_superuser or self.request.user.is_admin:
            try:
                instance = self.queryset.get(id=self.kwargs["id"])
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            instance.active = False
            instance.save()
            return Response({"Skill Deactivate": "Access Granted"}, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class IntershalaEmployeeViewSets(viewsets.ModelViewSet):
    queryset = IntershalaEmployee.objects.all().order_by('-created_at')
    serializer_class = IntershalaEmployeeSerializer

    def list(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_admin:
            query = IntershalaEmployee.objects.all()
            serializer = self.get_serializer(query, many=True)
            return Response(serializer.data, status=200)

    def perform_create(self, serializer):
        if self.request.user.is_superuser or self.request.user.is_admin:
            serializer = self.get_serializer(data=self.request.data)
            if serializer.is_valid(raise_exception=True):
                user_query = User.objects.get(id=self.request.data.get('user'))
                user_query.is_employee = True
                user_query.is_student = False
                user_query.save()
                serializer.save(first_name=user_query.first_name, last_name=user_query.last_name, active=True,
                                user=user_query)
                try:
                    qrcode_img = qrcode.make(self.request.data['first_name'] + " employee")
                    canvas = Image.new('RGB', (290, 290), 'white')
                    draw = ImageDraw.Draw(canvas)
                    canvas.paste(qrcode_img)
                    username = self.request.data['first_name']
                    fname = f'intershala_code-{username}' + '.png'
                    buffer = BytesIO()
                    canvas.save(buffer, 'PNG')
                    user_query.qr_code.save(fname, File(buffer), save=True)
                    canvas.close()
                except:
                    pass
                return Response(serializer.data, status=200)
            elif not serializer.is_valid:
                return Response(serializer.errors)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_admin:
            try:
                instance = self.queryset.get(id=self.kwargs["id"])
                user_query = User.objects.get(id=instance.user.id)
                user_query.is_employee = False
                user_query.is_student = True
                user_query.save()
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            instance.delete()
            return Response({"Employee Deleted": "Access Granted"}, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def update(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_admin:
            try:
                instance = IntershalaEmployee.objects.get(id=self.kwargs["id"])
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            serializer = self.get_serializer(instance, data=self.request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(updated_at=datetime.now())
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=401)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class IntershalaEmployeeProfileViewSets(generics.RetrieveUpdateAPIView):
    queryset = IntershalaEmployee.objects.all()
    serializer_class = IntershalaEmployeeSerializer

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_employee:
            try:
                instance = IntershalaEmployee.objects.get(user=self.request.user.id)
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def update(self, request, *args, **kwargs):
        if self.request.user.is_employee:
            try:
                instance = IntershalaEmployee.objects.get(user=self.request.user.id)
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=400)
            serializer = self.get_serializer(instance, data=self.request.data, partial=True)
            user_query = User.objects.get(id=self.request.user.id)
            if serializer.is_valid(raise_exception=True):
                data = serializer.save(updated_at=datetime.now())
                user_query.username = data.first_name
                user_query.first_name = data.first_name
                user_query.last_name = data.last_name
                user_query.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=401)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
