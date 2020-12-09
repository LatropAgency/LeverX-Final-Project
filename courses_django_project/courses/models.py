import os

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User


def get_upload_path_doc(self, filename):
    return os.path.join(self.doc_path(), filename)


class TextModel(models.Model):
    text = models.TextField()


class Course(models.Model):
    title = models.CharField(max_length=256)
    participants = models.ManyToManyField(User)


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic = models.CharField(max_length=256)
    document = models.FileField(upload_to=get_upload_path_doc)

    def doc_path(self):
        return os.path.join(f'documents/{self.course_id}')


class Task(TextModel):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)


class Solution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()


class Mark(models.Model):
    solution = models.OneToOneField(Solution, on_delete=models.CASCADE)
    result = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])


class Comment(TextModel):
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
