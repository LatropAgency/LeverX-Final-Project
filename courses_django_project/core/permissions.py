from rest_framework.permissions import BasePermission, SAFE_METHODS

from courses.models import (
    Lecture,
    Course,
    Task,
)

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
    def has_object_permission(self, request, view, obj):
        if issubclass(type(obj), Course):
            return request.user in obj.participants.all()
        if issubclass(type(obj), Lecture):
            return request.user in obj.course.participants.all()
        if issubclass(type(obj), Task):
            return request.user in obj.lecture.course.participants.all()
        else:
            return False
