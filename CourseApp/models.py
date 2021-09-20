from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser

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
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    raters = models.FloatField(default=1)
    rating = models.IntegerField(default=1)
    price = models.FloatField(default=0)
    OFFLINE = 0
    ONLINE = 1
    COURSE_TYPE_CHOICES = [(ONLINE, 'Online'), (OFFLINE, 'Offline')]
    course_type = models.IntegerField(choices=COURSE_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} with type {self.course_type}"

    class Meta:
        ordering = ['-id']


class OfflineCourse(models.Model):
    course = models.OneToOneField(Course, on_delete=models.PROTECT, primary_key=True, related_name="offline", default=1)
    e_time = models.TimeField()
    b_time = models.TimeField()
    e_date = models.DateField()
    b_date = models.DateField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"located in: {self.location} , begins on: {self.b_date} on " \
               f"{self.b_time}, ends on {self.e_date} on {self.e_time}"


class OnlineCourse(models.Model):
    course = models.OneToOneField(Course, on_delete=models.PROTECT, primary_key=True, related_name="online", default=1)
    type = models.CharField(max_length=30)
    duration = models.CharField(max_length=50)
    lessons_count = models.IntegerField()

    def __str__(self):
        return f"Course type: {self.type} with duration(in seconds): " \
               f"{self.duration}s and has {self.lessons_count} lessons"


class UserSegment(models.Model):
    name = models.CharField(max_length=30)
    segment = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)

    uid = models.CharField(max_length=50)
    source = models.CharField(max_length=50, null=True)
    info_complete = models.BooleanField(default=False)
    token = models.CharField(max_length=15, null=True)
    GENDER_CHOICES = [(0, 'Male'), (1, 'Female')]

    first_name = models.CharField(max_length=50, null=True)
    second_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)

    gender = models.IntegerField(choices=GENDER_CHOICES, null=True)
    age_group = models.CharField(max_length=50, null=True)
    level = models.IntegerField(null=True)

    segment = models.ForeignKey(UserSegment, on_delete=models.PROTECT, null=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    courses = models.ManyToManyField(Course, through="UserJoinsCourse")

    username = models.CharField(
        'username',
        default="noUsername",
        max_length=150,
        unique=False,
        null=True,
        blank=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}, {self.gender} with age group: {self.age_group}, has phone: {self.phone} and his info is' \
               f'{" not" if self.info_complete == False else ""} completed'


class Payment(models.Model):
    amount = models.FloatField()

    def __str__(self):
        return self.amount


class UserJoinsCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT)
    last_unlocked = models.IntegerField()

    class Meta:
        unique_together = (('user', 'course'),)

    def __str__(self):
        return self.last_unlocked


class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return f'user id: {self.user} made comment At {self.date} with text: {self.text} ' \
               f'on the course with id: {self.course}'


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


class Exam(models.Model):
    num_q = models.IntegerField()
    online_coruse = models.ForeignKey(OnlineCourse, on_delete=models.PROTECT)

    def __str__(self):
        return f'exam with num_q = {self.num_q}'


class Attempt(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'exam id: {self.exam} preformed by user id: {self.user}'


class Choice(models.Model):
    text = models.TextField()
    question = models.ForeignKey('Question', on_delete=models.PROTECT, related_name="Question")

    def __str__(self):
        return self.text


class Question(models.Model):
    text = models.TextField()
    exam = models.ForeignKey(Exam, on_delete=models.PROTECT)
    answer_choice = models.ForeignKey(Choice, on_delete=models.PROTECT, related_name="Choice")

    def __str__(self):
        return self.text


class AttemptSolveQuestion(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    picked_choice = models.ForeignKey(Choice, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('attempt', 'question', "picked_choice"),)

    def __str__(self):
        return f'attempt id: {self.attempt} for question id: {self.question}' \
               f'and picked choice id: {self.picked_choice}'


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    online_course = models.ForeignKey(OnlineCourse, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.title}, {self.description}'


class PDF(models.Model):
    path = models.URLField(max_length=200)
    name = models.CharField(max_length=100)
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)

    def __str__(self):
        return f'pdf name: {self.name} in path: {self.name}'


class Media(models.Model):
    path = models.URLField(max_length=200)
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT)

    def __str__(self):
        return f'Media path: {self.path} for lesson id: {self.lesson}'
