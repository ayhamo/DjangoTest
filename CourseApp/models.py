from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    # id is always auto generated
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.url


class Category(models.Model):
    cname = models.CharField(max_length=50)
    imgID = models.ForeignKey(Image, on_delete=models.PROTECT)

    def __str__(self):
        return self.cname


class Course(models.Model):
    name = models.CharField(max_length=30)
    CourseType = models.CharField(max_length=8)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name} with type {self.CourseType}"


class OfflineCourse(models.Model):
    CourseID = models.ForeignKey(Course, on_delete=models.PROTECT, primary_key=True)
    e_time = models.TimeField()
    b_time = models.TimeField()
    e_date = models.DateField()
    b_date = models.DateField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"located in: {self.location} , begins on: {self.b_date} on " \
               f"{self.b_time}, ends on {self.e_date} on {self.e_time}"


class OnlineCourse(models.Model):
    CourseID = models.ForeignKey(Course, on_delete=models.PROTECT, primary_key=True)
    raters = models.FloatField()
    rating = models.IntegerField()
    type = models.CharField(max_length=30)
    duration = models.CharField(max_length=50)
    lessons_count = models.IntegerField()

    def __str__(self):
        return f"Course type: {self.type} with duration(in seconds): " \
               f"{self.duration}s and has {self.lessons_count} lessons" \
               f"and {self.raters} have rated it"


class UserSegment(models.Model):
    name = models.CharField(max_length=30)
    segmentID = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class user(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    segmentID = models.ForeignKey(UserSegment, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f'At {self.date} with text: {self.text}'


class Payment(models.Model):
    amount = models.FloatField()
    userID = models.ForeignKey(user, on_delete=models.PROTECT)

    def __str__(self):
        return self.amount


class UserJoinsCourseWpayment(models.Model):
    userID = models.ForeignKey(user, on_delete=models.PROTECT)
    courseID = models.ForeignKey(Course, on_delete=models.PROTECT)
    paymentID = models.ForeignKey(Payment, on_delete=models.PROTECT)
    last_unlocked = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('userID', 'courseID', "paymentID"),)

    def __str__(self):
        return self.last_unlocked


class SurveyNote(models.Model):
    note = models.TextField()
    courseID = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.note


class SurveyQuestion(models.Model):
    question = models.TextField()
    courseID = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.question


class SurveyChoice(models.Model):
    choice = models.TextField()
    courseID = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.choice


class Survey(models.Model):
    count = models.IntegerField()
    questionID = models.ForeignKey(SurveyQuestion, on_delete=models.PROTECT)
    choiceID = models.ForeignKey(SurveyChoice, on_delete=models.PROTECT)
    courseID = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.count


class UserCommentedOnCourse(models.Model):
    userID = models.ForeignKey(user, on_delete=models.PROTECT)
    commentID = models.ForeignKey(Comment, on_delete=models.PROTECT)
    courseID = models.ForeignKey(Course, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('userID', 'commentID', "courseID"),)

    def __str__(self):
        return f'user id: {self.userID} made a comment with id {self.commentID}' \
               f'on the course with id: {self.courseID}'


class Exam(models.Model):
    num_q = models.IntegerField()

    def __str__(self):
        return f'exam with num_q = {self.num_q}'


class Attempt(models.Model):
    examID = models.ForeignKey(Exam, on_delete=models.PROTECT)
    userID = models.ForeignKey(user, on_delete=models.PROTECT)

    def __str__(self):
        return f'exam id: {self.examID} preformed by user id: {self.userID}'


class Choice(models.Model):
    text = models.TextField()
    questionID = models.ForeignKey('Question', on_delete=models.PROTECT)

    def __str__(self):
        return self.text


class Question(models.Model):
    text = models.TextField()
    examID = models.ForeignKey(Exam, on_delete=models.PROTECT)
    ansChoiceID = models.ForeignKey(Choice, on_delete=models.PROTECT)

    def __str__(self):
        return self.text


class AttemptSolveQuestion(models.Model):
    attemptID = models.ForeignKey(Attempt, on_delete=models.PROTECT)
    questionID = models.ForeignKey(Question, on_delete=models.PROTECT)
    pickedChoiceID = models.ForeignKey(Choice, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('attemptID', 'questionID', "pickedChoiceID"),)

    def __str__(self):
        return f'attempt id: {self.attemptID} for question id: {self.questionID}' \
               f'and picked choice id: {self.pickedChoiceID}'


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    OnlineCourseID = models.ForeignKey(OnlineCourse, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.title}, {self.description}'


class PDF(models.Model):
    path = models.CharField(max_length=500)
    name = models.CharField(max_length=100)
    lessonID = models.ForeignKey(Lesson, on_delete=models.PROTECT)

    def __str__(self):
        return f'pdf name: {self.name} in path: {self.name}'


class Media(models.Model):
    path = models.CharField(max_length=500)
    lessonID = models.ForeignKey(Lesson, on_delete=models.PROTECT)

    def __str__(self):
        return f'Media path: {self.path} for lesson id: {self.lessonID}'
