from django.contrib import admin
from django.contrib.auth.models import Group
from .models import NewUser, Course, Account, Activation, JoinedCourse, \
    Topic, Heading, CompQuestion, CompQuesTestCase, CompResult, \
    WeekTest, WeekTestQuestion, WeekTestResult, Feedback


class AccountA(admin.ModelAdmin):
    list_display = ('email','fname', 'lname', 'password')
class TopicA(admin.ModelAdmin):
    list_display = ('id', 'topicLabel','course')
    list_filter = ('course',)
class HeadingA(admin.ModelAdmin):
    list_display = ('topic', 'headingLabel')
    list_filter = ('topic',)

class CourseA(admin.ModelAdmin):
    list_display = ('courseID', 'courseName')
class JoinedCourseA(admin.ModelAdmin):
    list_display = ('email','joinedCourse')
    list_filter = ('email','joinedCourse')

class WeekTestA(admin.ModelAdmin):
    list_display = ('course','test_id')
    list_filter = ('course','date_added')
class FeedbackA(admin.ModelAdmin):
    list_display = ('feedback_id','rating')
    list_filter = ('rating',)
class CompQuestionA(admin.ModelAdmin):
    list_display = ('comp_id','date_added')
    list_filter = ('date_added', 'comp_id')
class CompQuesTestCaseA(admin.ModelAdmin):
    list_display = ('testcase_id','competitionQuestion')
    list_filter = ('competitionQuestion', 'testcase_id')
class CompResultA(admin.ModelAdmin):
    list_display = ('user','competitionQuestion', 'passed', 'result')
    list_filter = ('competitionQuestion', 'user', 'passed', 'result')
class WeekTestQuestionA(admin.ModelAdmin):
    list_display = ('test','question_id', 'question_text')
    list_filter = ('test','question_id', 'question_text')
class WeekTestResultA(admin.ModelAdmin):
    list_display = ('test','user', 'result', 'marks')
    list_filter = ('test','user', 'result', 'marks')

# Register your models here.
# admin.site.unregister(Group)
admin.site.register(NewUser)
admin.site.register(Course, CourseA)
admin.site.register(Account, AccountA)
admin.site.register(Activation)
admin.site.register(JoinedCourse, JoinedCourseA)
admin.site.register(Heading, HeadingA)
admin.site.register(Topic, TopicA)
admin.site.register(CompQuestion, CompQuestionA)
admin.site.register(CompQuesTestCase, CompQuesTestCaseA)
admin.site.register(CompResult, CompResultA)
admin.site.register(WeekTest, WeekTestA)
admin.site.register(WeekTestQuestion, WeekTestQuestionA)
admin.site.register(WeekTestResult)
admin.site.register(Feedback, FeedbackA)


admin.site.site_header = "Techomato Administration"
admin.site.site_title = 'Techomato Administration'
admin.site.index_title = 'Techomato'
admin.empty_value_display = '**Empty**'