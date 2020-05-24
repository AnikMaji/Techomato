from django.db import models
from django import forms

class NewUser(models.Model):
    email = models.EmailField(max_length=50, primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    rpassword = models.CharField(max_length=15)
    image = models.ImageField(upload_to='pics/', default="pics/user.png")
class NewForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = ['email','fname','lname','password','phone','rpassword']

class Account(models.Model):
    email = models.EmailField(max_length=50, primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    image = models.ImageField(upload_to='pics/', default="pics/user.png")

class Activation(models.Model):
    email = models.EmailField(max_length=50, primary_key=True)
    otp = models.CharField(max_length=6)
    is_activated=models.BooleanField()

class Course(models.Model):
    courseID=models.CharField(max_length=50, primary_key=True, auto_created=True)
    courseName=models.CharField(max_length=50)
    courseType = models.CharField(max_length=50)
    courseCat = models.CharField(max_length=50)
    courseDescription = models.TextField()
    courseLink=models.CharField(max_length=50)
    image = models.ImageField(upload_to='coursePics/')


class JoinedCourse(models.Model):
    email = models.EmailField(max_length=50)
    is_joined=models.BooleanField()
    joinedCourse=models.CharField(max_length=50)

class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    id=models.CharField(max_length=50, primary_key=True, auto_created=True)
    topicLabel=models.CharField(max_length=255, null=False)

class Heading(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=False)
    headingId=models.CharField(primary_key=True, max_length=55, auto_created=True)
    headingLabel=models.CharField(max_length=255, null=False)
    headingText=models.TextField(null=False)


class CompQuestion(models.Model):
    comp_id=models.CharField(max_length=50, primary_key=True, auto_created=True, null=False)
    date_added=models.DateField(null=False)
    question=models.TextField(null=False)
    input_pattern=models.TextField(null=False)
    output_pattern=models.TextField(null=False)

class CompQuesTestCase(models.Model):
    competitionQuestion=models.ForeignKey(CompQuestion, on_delete=models.CASCADE, null=False)
    testcase_id=models.CharField(max_length=50, primary_key=True, auto_created=True, null=False)
    id=models.PositiveIntegerField(null=False, auto_created=True)
    input=models.TextField(default="")
    output=models.TextField(null=False)

class CompResult(models.Model):
    competitionQuestion=models.ForeignKey(CompQuestion, on_delete=models.CASCADE, null=False)
    user=models.CharField(max_length=55, null=False)
    result=models.PositiveIntegerField()
    passed=models.PositiveIntegerField()

class WeekTest(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    test_id=models.CharField(max_length=55, null=False, primary_key=True)
    test_category=models.CharField(max_length=55, null=False)
    full_marks=models.PositiveIntegerField()
    date_added=models.DateField()

class WeekTestQuestion(models.Model):
    test=models.ForeignKey(WeekTest, on_delete=models.CASCADE, null=False)
    question_id=models.CharField(max_length=55, null=False, primary_key=True)
    question_text=models.TextField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    choose = (('A', 'option1'), ('B', 'option2'), ('C', 'option3'), ('D', 'option4'))
    answer = models.CharField(max_length=1, choices=choose)

class WeekTestResult(models.Model):
    test=models.ForeignKey(WeekTest, on_delete=models.CASCADE, null=False)
    user=models.CharField(max_length=55, null=False, primary_key=True)
    result=models.PositiveIntegerField()
    marks=models.PositiveIntegerField()

class Feedback(models.Model):
    feedback_id=models.CharField(max_length=55, null=False, auto_created=True, primary_key=True)
    test_comp=models.CharField(max_length=55, null=False)
    study_materials=models.CharField(max_length=55, null=False)
    compiler=models.CharField(max_length=55, null=False)
    overall=models.CharField(max_length=55, null=False)
    suggestion=models.TextField()
    comment=models.TextField()
    rating=models.IntegerField()