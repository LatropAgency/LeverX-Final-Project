from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from courses.models import Course

from users.enum_types import RoleTypes


class TeacherOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleTypes.TEACHER.value


class StudentOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleTypes.STUDENT.value


class TeacherOrStudentReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleTypes.TEACHER.value or request.method in SAFE_METHODS


class StudentOrTeacherReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleTypes.STUDENT.value or request.method in SAFE_METHODS


class IsParticipant(BasePermission):
    def has_permission(self, request, view):
        course = get_object_or_404(Course, pk=view.kwargs['course_pk'])
        return request.user in course.participants.all()
