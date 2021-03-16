from datetime import datetime
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from user.models import User
from .models import *
from rest_framework.response import Response
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from intershala_admin.models import AdminNotification

from intershala_admin.models import IntershalaCompany

from student.models import Student


class RecruiterSignin(generics.CreateAPIView):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSignINSerializer

    def perform_create(self, serializer):
        try:
            user = User.objects.create_user(username=self.request.data['first_name'],
                                            password=self.request.data['password'],
                                            first_name=self.request.data['first_name'],
                                            last_name=self.request.data['last_name'],
                                            email=self.request.data['email'],
                                            is_recruiter=False)
            try:
                qrcode_img = qrcode.make(self.request.data['first_name'] + " recruiter")
                canvas = Image.new('RGB', (290, 290), 'white')
                draw = ImageDraw.Draw(canvas)
                canvas.paste(qrcode_img)
                username = self.request.data['first_name']
                fname = f'intershala_code-{username}' + '.png'
                buffer = BytesIO()
                canvas.save(buffer, 'PNG')
                user.qr_code.save(fname, File(buffer), save=True)
                canvas.close()
            except:
                pass
        except IntegrityError:
            return Response({"RECRUITER_EXISTS": "Recruiter already exists with this Email."}, status=400)
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save(user=user, active=False)
            recruiter_query = Recruiter.objects.get(id=data.id)
            if data:
                company_query = IntershalaCompany.objects.get(id=self.request.data.get('company'))
                company_query.recruiter.add(data)
                AdminNotification.notify_admin(recruiter=recruiter_query,
                                               recruiter_name=self.request.data.get('first_name'))
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)


class RecruiterNotificationViewSets(generics.ListAPIView):
    queryset = RecruiterNotification.objects.all().order_by('-created_at')
    serializer_class = RecruiterNotificationSerializers
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            queryset = RecruiterNotification.objects.filter(
                recruiter=Recruiter.objects.get(user=self.request.user.id)).order_by('-created_at')
            queryset.update(seen=True)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class RecruiterProfile(generics.RetrieveAPIView, generics.RetrieveUpdateAPIView):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterProfileSerializer
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            recruiter_query = Recruiter.objects.get(user=self.request.user)
            if recruiter_query.active:
                serializer = self.get_serializer(recruiter_query)
                return Response(serializer.data, status=200)
            elif not recruiter_query.active:
                return Response({"NO_ACCESS": "Access Denied"}, status=401)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def update(self, request, *args, **kwargs):
        if self.request.user.is_recruiter:
            recruiter_query = Recruiter.objects.get(user=self.request.user)
            if recruiter_query.active:
                serializer = self.get_serializer(recruiter_query, data=self.request.data, partial=True)
                user_query = User.objects.get(id=self.request.user.id)
                if serializer.is_valid(raise_exception=True):
                    data = serializer.save(updated_at=datetime.now())
                    user_query.username = data.first_name
                    user_query.first_name = data.first_name
                    user_query.last_name = data.last_name
                    user_query.save()
                    return Response(serializer.data, status=200)
                else:
                    return Response(serializer.errors, status=400)
            elif not recruiter_query.active:
                return Response({"NO_ACCESS": "Access Denied"}, status=401)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)


class RecruiterReviewViewsets(generics.ListCreateAPIView):
    queryset = RecruiterReview.objects.all().order_by('created_at')
    serializer_class = RecruiterReviewSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        if self.request.user.is_student:
            serializer = self.get_serializer(data=self.request.data)
            if serializer.is_valid(raise_exception=True):
                student_query = Student.objects.get(user=self.request.user)
                serializer.save(student=student_query)
                Recruiter.rating_counter(self=self, recruiter_id=serializer.validated_data.get('recruiter').id)
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=401)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

    def list(self, request, *args, **kwargs):
        if self.request.user.is_student:
            queryset = RecruiterReview.objects.filter(student=Student.objects.get(user=self.request.user)).order_by(
                'created_at')
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
