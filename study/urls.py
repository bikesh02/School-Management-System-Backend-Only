from django.contrib import admin
from .views import *
from django.urls import path
from rest_framework.routers import SimpleRouter

router= SimpleRouter()

router.register('student', StudentView)
router.register('teacher', TeacherView)
router.register('class', ClassView)
router.register('assignment', AssignmentView)
router.register('submission', SubmissionView)
router.register('academicrecord', AcademicRecordView)
router.register('attendance', AttendanceView)
router.register('examination', ExaminationView)
router.register('book', BookView)
router.register('borrow', BorrowView)

urlpatterns = [
    
]+ router.urls
