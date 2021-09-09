from django.db import models
from django.contrib.auth.models import User

"""ID's are always generated auto as PK if no PK is specified"""
"""all FK's references in database add X_id as default"""


class Image(models.Model):
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.url


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    img = models.ForeignKey(Image, on_delete=models.PROTECT)

    def __str__(self):
        return self.category_name


class Course(models.Model):
    name = models.CharField(max_length=30)
    course_type = models.CharField(max_length=8)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name} with type {self.course_type}"


class OfflineCourse(models.Model):
    Course = models.ForeignKey(Course, on_delete=models.PROTECT, primary_key=True)
    e_time = models.TimeField()
    b_time = models.TimeField()
    e_date = models.DateField()
    b_date = models.DateField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"located in: {self.location} , begins on: {self.b_date} on " \
               f"{self.b_time}, ends on {self.e_date} on {self.e_time}"


class OnlineCourse(models.Model):
    Course = models.ForeignKey(Course, on_delete=models.PROTECT, primary_key=True)
    raters = models.FloatField()
    rating = models.IntegerField()
    type = models.CharField(max_length=30)
    duration = models.CharField(max_length=50)
    lessons_count = models.IntegerField()

    def __str__(self):
        return f"Course type: {self.type} with duration(in seconds): " \
               f"{self.duration}s and has {self.lessons_count} lessons" \
               f"and {self.raters} have rated it."


class UserSegment(models.Model):
    name = models.CharField(max_length=30)
    segment = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class user(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    segment = models.ForeignKey(UserSegment, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f'At {self.date} with text: {self.text} and thats it'


class Payment(models.Model):
    amount = models.FloatField()
    user = models.ForeignKey(user, on_delete=models.PROTECT)

    def __str__(self):
        return self.amount


class UserJoinsCourse(models.Model):
    user = models.ForeignKey(user, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT)
    last_unlocked = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'course'),)

    def __str__(self):
        return self.last_unlocked


class SurveyNote(models.Model):
    note = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.note


class SurveyQuestion(models.Model):
    question = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.question


class SurveyChoice(models.Model):
    choice = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.choice


class Survey(models.Model):
    count = models.IntegerField()
    question = models.ForeignKey(SurveyQuestion, on_delete=models.PROTECT)
    choice = models.ForeignKey(SurveyChoice, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.count


class UserCommentedOnCourse(models.Model):
    user = models.ForeignKey(user, on_delete=models.PROTECT)
    comment = models.ForeignKey(Comment, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('user', 'comment', "course"),)

    def __str__(self):
        return f'user id: {self.user} made a comment with id {self.comment}' \
               f'on the course with id: {self.course}'


class Exam(models.Model):
    num_q = models.IntegerField()

    def __str__(self):
        return f'exam with num_q = {self.num_q}'


class Attempt(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.PROTECT)
    user = models.ForeignKey(user, on_delete=models.PROTECT)

    def __str__(self):
        return f'exam id: {self.exam} preformed by user id: {self.user}'


class Choice(models.Model):
    text = models.TextField()
    question = models.ForeignKey('Question', on_delete=models.PROTECT, related_name="myQuestion")

    def __str__(self):
        return self.text


class Question(models.Model):
    text = models.TextField()
    exam = models.ForeignKey(Exam, on_delete=models.PROTECT)
    answer_choice = models.ForeignKey(Choice, on_delete=models.PROTECT, related_name="myChoice")

    def __str__(self):
        return self.text


class AttemptSolveQuestion(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    pickedChoice = models.ForeignKey(Choice, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('attempt', 'question', "pickedChoice"),)

    def __str__(self):
        return f'attempt id: {self.attempt} for question id: {self.question}' \
               f'and picked choice id: {self.pickedChoice}'


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    online_course = models.ForeignKey(OnlineCourse, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.title}, {self.description}'


class PDF(models.Model):
    path = models.CharField(max_length=500)
    name = models.CharField(max_length=100)
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)

    def __str__(self):
        return f'pdf name: {self.name} in path: {self.name}'


class Media(models.Model):
    path = models.CharField(max_length=500)
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)

    def __str__(self):
        return f'Media path: {self.path} for lesson id: {self.lesson}'
