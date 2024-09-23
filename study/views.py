from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework import viewsets,mixins,generics,status
from rest_framework.response import Response
from .serializers import *
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView


# Create your views here.

class StudentView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    search_fields =['first_name']
    
    
class TeacherView(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    
    
class ClassView(viewsets.ModelViewSet):
    serializer_class = ClassSerializer
    queryset = Class.objects.all()
    
    
class AssignmentView(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
    
class SubmissionView(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()
    
class AcademicRecordView(viewsets.ModelViewSet):
    serializer_class = AcademicRecordSerializer
    queryset = AcademicRecord.objects.all()
    
    
class AttendanceView(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()
    
    
class ExaminationView(viewsets.ModelViewSet):
    serializer_class = ExaminationSerializer
    queryset = Examination.objects.all()
    
    
class BookView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    
    
class BorrowView(viewsets.ModelViewSet):
    serializer_class = BorrowSerializer
    queryset = Borrow.objects.all()