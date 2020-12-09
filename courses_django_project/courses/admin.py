from django.contrib import admin
from courses.models import Course, Task, Lecture

admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Task)
