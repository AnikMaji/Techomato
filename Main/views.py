import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
import re
from .email import Email
from django.shortcuts import render
from .decode import Decode
import smtplib
import requests
from . import executor
from .compiler import MyCompiler
from django.contrib import messages
from .models import NewUser, NewForm, Activation, Account, JoinedCourse, \
    Course, Topic, Heading, CompResult, CompQuesTestCase, CompQuestion, \
    WeekTestQuestion, WeekTestResult, WeekTest, Feedback
from time import sleep

email = ''
id = 0


def delete_all(request):
    NewUser.objects.all().delete()
    Activation.objects.all().delete()
    Account.objects.all().delete()
    return redirect('/')


def del_otp(email):
    sleep(300)
    Activation.objects.filter(email=email).delete()


def del_temp_user(email):
    NewUser.objects.filter(email=email).delete()

def index(request):
    try:
        a=request.session['userID']
        b=request.session['userName']
        c=request.session['userfName']
        d=request.session['logged_in']
        e=request.session['logged_out']
    except:
        request.session['logged_in']=False
    try:
        a=Course.objects.all()[:3]
        b=Course.objects.all()[len(Course.objects.all())-2:]
        return render(request, 'index.html', {'courses': a, 'newcourses':b})
    except:
        return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        a = NewUser.objects.filter(email=email)
        for x in a:
            user = x
        if (len(a) == 1):
            if (user.password == password):
                request.session['userID'] = email
                request.session['userName'] = user.fname + " " + user.lname
                request.session['userfName'] = user.fname
                request.session['logged_in'] = True
                request.session['logged_out'] = False
                if (request.session['userID']):
                    a1 = Activation.objects.filter(email=request.session['userID'])
                    for x in a1:
                        a = x
                    if (a.is_activated):
                        return redirect('/dashboard/')
                    else:
                        return redirect('/activate/')
                else:
                    redirect('/register/')
            else:
                return render(request, 'login2.html',
                              {'mymsg': "Password doesn't match", 'loggedin': False, 'loggedout': False})
        else:
            return render(request, 'login2.html', {'mymsg': "User doesn't exist", 'loggedin': False, 'loggedout': False})
    elif request.method == 'GET':
        try:
            if (request.session['logged_out']):
                del request.session['logged_out']
                return render(request, 'login2.html', {'loggedout': True})
            else:
                return render(request, 'login2.html', {'loggedout': False})
        except:
            return render(request, 'login2.html', {'loggedout': False})


def logout(request):
    if (request.session.get('logged_in')):
        del request.session['userID']
        del request.session['userfName']
        del request.session['userName']
        request.session['logged_in'] = False
        request.session['logged_out'] = True
        return redirect('/login/')
        # return login(request, ss="You are successfully logged out.")


def validateName(name):
    if (' ' in name):
        names = name.split()
    else:
        names = [name]
    for name in names:
        if (name.isalpha()):
            return True
        else:
            print('name prblm')
            return False


def validateDob(dob):
    from datetime import datetime
    date_string = dob
    date_string2 = "2020-04-22 00:00:00"
    dt = datetime.fromisoformat(date_string)
    dt2 = datetime.fromisoformat(date_string2)
    if (dt.date() > dt2.date()):
        print('dob prblm')
        return False
    else:
        return True


def validateEmail(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex, email)):
        return True
    else:
        print('email prblm')
        return False


def validatePN(pn):
    if (pn.isnumeric()):
        res = requests.get(
            "http://apilayer.net/api/validate?access_key=86ef7c20efe78fe00b1ef87caf75ef76&number=91" + pn + "&country_code=&format=1")
        resJson = res.json()
        if (resJson['valid'] == True):
            return True
        else:
            print('pn prblm')
            return False
    else:
        return False


def validatePassword(pwd, rpwd):
    if (len(pwd) > 5):
        if (pwd == rpwd):
            return True
        else:
            return False
    else:
        return False


def register(request):
    global email, id
    if request.method == 'POST':
        em = Email()
        form = NewForm(request.POST, request.FILES)
        print(request.FILES)
        a = form.data.dict()
        print(a)
        # file = a['image']
        # print(file)
        fname = str(a['fname'])
        lname = str(a['lname'])
        email = str(a['email'])
        pn = str(a['phone'])
        pwd = str(a['password'])
        rpwd = str(request.POST['rpassword'])
        print(fname, lname, email, pn, pwd, rpwd)
        #
        # print(form.data.dict()['name'])

        if (validateName(fname)):
            if(validateName(lname)):
                if(validateEmail(email)):
                    if(validatePassword(pwd, rpwd)):
                        if(validatePN(pn)):
                            if(form.is_valid()):
                                    otp = em.generate_otp()
                                    executor.submit(em.sendOTP, otp)
                                    form.save()
                                    ac = Activation(email, otp, False)
                                    ac.save()
                                    User = NewUser.objects.filter(email=email)
                                    for x in User:
                                        user = x
                                    request.session['userID'] = email
                                    request.session['userName'] = user.fname + " " + user.lname
                                    request.session['userfName'] = user.fname
                                    request.session['logged_in'] = True
                                    return redirect('/activate/')
                            else:
                                print(form.errors)
                                return render(request, 'register2.html', {'mymsg': form.errors, 'logged':False})
                        else:
                            return render(request, 'register2.html', {'mymsg': 'Invalid Phone Number', 'logged': False})
                    else:
                        return render(request, 'register.html', {'mymsg': 'Invalid Password', 'logged': False})
                else:
                    return render(request, 'register2.html', {'mymsg': 'Invalid Email ID', 'logged': False})
            else:
                return render(request, 'register2.html', {'mymsg': 'Invalid Last Name', 'logged': False})
        else:
            return render(request, 'register2.html', {'mymsg': 'Invalid First Name', 'logged': False})


    elif request.method == 'GET':
        if(request.session['logged_in']):
            return render(request, 'register2.html', {'mymsg': "You are already logged in.", 'logged': True})
        else:
            return render(request, 'register2.html', {'logged':False})


def dashboard(request):
    if (request.method == "GET"):
        if (request.session['logged_in']):
            try:
                data = Account.objects.get(email=request.session['userID'])
                joinedCourse=JoinedCourse.objects.filter(email=data.email)
                testData=[]
                for x in joinedCourse:
                    try:
                        test=WeekTest.objects.get(course__courseID=x.joinedCourse, date_added=datetime.datetime.today())
                        print(test)
                        testData.append(test)
                    except:
                        pass
                testResults=WeekTestResult.objects.filter(user=request.session['userID'])
                compss=CompQuestion.objects.filter(date_added=datetime.datetime.today())
                print(testData)

                return render(request, 'dashboard.html',{'user':data, 'lentestData':len(testData),'testData':testData,'lennew':len(compss) ,'new':compss, 'lenres':len(testResults),'testResults': testResults})
            except:
                return redirect('/login/')
        else:
            return redirect('/login/')


def activate(request):
    global email
    if (request.method == 'POST'):
        otp = request.POST['otp']
        User = Activation.objects.filter(email=request.session['userID'])
        for x in User:
            user = x
        if (user.otp == otp):
            Activation.objects.filter(email=request.session['userID']).update(is_activated=True)
            em = Email()
            em.sendSuccessEmail(request.session['userID'])
            mainUser = NewUser.objects.filter(email=request.session['userID'])
            for x in mainUser:
                account = Account(fname=x.fname, lname=x.lname, email=x.email, phone=x.phone, password=x.password,
                                  image=x.image)
                account.save()
            return redirect("/dashboard/")
        else:
            return redirect('/activate/')
    elif (request.method == 'GET'):
        if (request.session['userID']):
            a1 = Activation.objects.filter(email=request.session['userID'])
            for x in a1:
                a = x
            if (len(a1) > 0):
                if (a.is_activated):
                    a = Account.objects.filter(email=request.session['userID'])
                    for x in a:
                        data = x
                    return render(request, 'dashboard.html', {'x': data})
                else:
                    return render(request, 'activation.html')
            else:
                return redirect('/register2/')
        else:
            return redirect('/login/')


def viewUsers(request):
    a = Account.objects.all()
    userDict = {}
    i = 0
    userDict['fname'] = []
    userDict['email'] = []
    userDict['lname'] = []
    userDict['password'] = []
    userDict['phone'] = []
    userDict['image'] = []
    for x in a:
        userDict['fname'].append(x.fname)
        userDict['lname'].append(x.lname)
        userDict['email'].append(x.email)
        userDict['password'].append(x.password)
        userDict['phone'].append(x.phone)
        userDict['image'].append(x.image.url)
    import pandas as pd
    df = pd.DataFrame(userDict)
    df.to_csv("data.csv")
    return render(request, 'view.html', {'data': a})


def courses(request):
    a=Course.objects.all()
    return render(request, 'courses.html',{'courses':a})


def studymaterials(request):
    if(request.method=="GET"):
        if(request.session['logged_in']):
            a=JoinedCourse.objects.filter(email=request.session['userID'])
            joinedCoursesIDs=[]
            topicsData = {}
            headingsData = {}
            for x in a:
                joinedCoursesIDs.append(x.joinedCourse)
                t = Topic.objects.filter(course__courseID=x.joinedCourse)
                topicsData[x.joinedCourse] = []

                for y in t:
                    h = Heading.objects.filter(topic=y)
                    topicsData[x.joinedCourse].append(y)
                    headingsData[y.id]=[]
                    for hh in h:
                        headingsData[y.id].append(hh)
            coursesData={}

            for x in joinedCoursesIDs:
                s=Course.objects.filter(courseID=x)

                for y in s:
                    coursesData[x]=y
            print(len(a))
            print(joinedCoursesIDs)
            print(coursesData)

            return render(request, 'studymaterials.html', {'coursesJoined':coursesData, 'topics':topicsData, 'headings':headingsData, 'length':len(a)})
        else:
            return redirect('/login/')



# def python3(request):
#     if(request.method=="GET"):
#         if request.session['logged_in']:
#             request.session['course_id']='course_01'
#             a=JoinedCourse.objects.filter(email=request.session['userID'])
#             for x in a:
#                 if(x.joinedCourse=='course_01'):
#                     a = JoinedCourse.objects.filter(email=request.session['userID'])
#                     joinedCoursesIDs = []
#                     for x in a:
#                         joinedCoursesIDs.append(x.joinedCourse)
#                     coursesData = {}
#                     for x in joinedCoursesIDs:
#                         s = Course.objects.filter(courseID=x)
#                         for y in s:
#                             coursesData[x] = y
#                     topics=Topic.objects.filter(course_id=request.session['course_id'])
#                     headings=[]
#                     for x in topics:
#                         h=Heading.objects.filter(topic=x)
#                         for x in h:
#                             headings.append(x)
#                     print(coursesData)
#                     print(topics)
#                     print(headings)
#                     return render(request,'python3.html',{'coursesJoined':coursesData, 'topics':topics, 'headings':headings, 'length':len(a), 'temp':"False"})
#
#             return render(request, 'pythonJoinCourse.html')
#         else:
#             return redirect("/login/")
#     # return render(request, 'python3.html')
#
#
# def java(request):
#     if(request.method=="GET"):
#         if request.session['logged_in']:
#             request.session['course_id']='course_02'
#             a=JoinedCourse.objects.filter(email=request.session['userID'])
#             for x in a:
#                 if(x.joinedCourse==request.session['course_id']):
#                     a = JoinedCourse.objects.filter(email=request.session['userID'])
#                     joinedCoursesIDs = []
#                     for x in a:
#                         joinedCoursesIDs.append(x.joinedCourse)
#                     coursesData = {}
#                     for x in joinedCoursesIDs:
#                         s = Course.objects.filter(courseID=x)
#                         for y in s:
#                             coursesData[x] = y
#                     topics = Topic.objects.filter(course_id=request.session['course_id'])
#                     headings = []
#                     for x in topics:
#                         h = Heading.objects.filter(topic=x)
#                         for x in h:
#                             headings.append(x)
#                     print(len(a))
#                     print(joinedCoursesIDs)
#                     print(coursesData)
#                     return render(request,'java.html',{'coursesJoined':coursesData, 'topics':topics, 'headings':headings, 'length':len(a), 'temp':"False"})
#
#             return render(request, 'javaJoinCourse.html')
#         else:
#             return redirect("/login/")
#
#
# def c(request):
#     if(request.method=="GET"):
#         if request.session['logged_in']:
#             request.session['course_id']='course_03'
#             a=JoinedCourse.objects.filter(email=request.session['userID'])
#             for x in a:
#                 if(x.joinedCourse==request.session['course_id']):
#                     a = JoinedCourse.objects.filter(email=request.session['userID'])
#                     joinedCoursesIDs = []
#                     for x in a:
#                         joinedCoursesIDs.append(x.joinedCourse)
#                     coursesData = {}
#                     for x in joinedCoursesIDs:
#                         s = Course.objects.filter(courseID=x)
#                         for y in s:
#                             coursesData[x] = y
#                     topics = Topic.objects.filter(course_id=request.session['course_id'])
#                     headings = []
#                     for x in topics:
#                         h = Heading.objects.filter(topic=x)
#                         for x in h:
#                             headings.append(x)
#                     print(len(a))
#                     print(joinedCoursesIDs)
#                     print(coursesData)
#                     return render(request,'c.html',{'coursesJoined':coursesData, 'topics':topics, 'headings':headings, 'length':len(a), 'temp':"False"})
#
#             return render(request, 'cJoinCourse.html')
#         else:
#             return redirect("/login/")
#
#
# def csharp(request):
#     if(request.method=="GET"):
#         if request.session['logged_in']:
#             request.session['course_id']='course_04'
#             a=JoinedCourse.objects.filter(email=request.session['userID'])
#             for x in a:
#                 if(x.joinedCourse==request.session['course_id']):
#                     a = JoinedCourse.objects.filter(email=request.session['userID'])
#                     joinedCoursesIDs = []
#                     for x in a:
#                         joinedCoursesIDs.append(x.joinedCourse)
#                     coursesData = {}
#                     for x in joinedCoursesIDs:
#                         s = Course.objects.filter(courseID=x)
#                         for y in s:
#                             coursesData[x] = y
#                     topics = Topic.objects.filter(course_id=request.session['course_id'])
#                     headings = []
#                     for x in topics:
#                         h = Heading.objects.filter(topic=x)
#                         for x in h:
#                             headings.append(x)
#                     print(len(a))
#                     print(joinedCoursesIDs)
#                     print(coursesData)
#                     return render(request,'csharp.html',{'coursesJoined':coursesData, 'topics':topics, 'headings':headings, 'length':len(a), 'temp':"False"})
#             print(request.session['course_id'])
#             return render(request, 'csharpJoinCourse.html')
#         else:
#             return redirect("/login/")
#
#
# def sql(request):
#     if(request.method=="GET"):
#         if request.session['logged_in']:
#             request.session['course_id']='course_05'
#             a=JoinedCourse.objects.filter(email=request.session['userID'])
#             for x in a:
#                 if(x.joinedCourse==request.session['course_id']):
#                     a = JoinedCourse.objects.filter(email=request.session['userID'])
#                     joinedCoursesIDs = []
#                     for x in a:
#                         joinedCoursesIDs.append(x.joinedCourse)
#                     coursesData = {}
#                     for x in joinedCoursesIDs:
#                         s = Course.objects.filter(courseID=x)
#                         for y in s:
#                             coursesData[x] = y
#                     topics = Topic.objects.filter(course_id=request.session['course_id'])
#                     headings = []
#                     for x in topics:
#                         h = Heading.objects.filter(topic=x)
#                         for x in h:
#                             headings.append(x)
#                     print(len(a))
#                     print(joinedCoursesIDs)
#                     print(coursesData)
#                     return render(request,'sql.html',{'coursesJoined':coursesData, 'topics':topics, 'headings':headings, 'length':len(a), 'temp':"False"})
#             print(request.session['course_id'])
#             return render(request, 'sqlJoinCourse.html')
#         else:
#             return redirect("/login/")
def subject(request, course_id):
    if(request.method=="GET"):
        if request.session['logged_in']:
            request.session['course_id']=course_id
            a=JoinedCourse.objects.filter(email=request.session['userID'])
            for x in a:
                if(x.joinedCourse==request.session['course_id']):
                    a = JoinedCourse.objects.filter(email=request.session['userID'])
                    joinedCoursesIDs = []
                    for x in a:
                        joinedCoursesIDs.append(x.joinedCourse)
                    coursesData = {}
                    for x in joinedCoursesIDs:
                        s = Course.objects.filter(courseID=x)
                        for y in s:
                            coursesData[x] = y
                    topics = Topic.objects.filter(course_id=request.session['course_id'])
                    headings = []
                    for x in topics:
                        h = Heading.objects.filter(topic=x)
                        for x in h:
                            x.headingText=x.headingText.split("\n")
                            headings.append(x)
                    print(len(a))
                    print(joinedCoursesIDs)
                    print(coursesData)
                    return render(request,'subject.html',{'coursesJoined':coursesData, 'topics':topics, 'headings':headings, 'length':len(a), 'temp':"False"})
            print(request.session['course_id'])
            c=Course.objects.get(courseID=course_id)
            return render(request, 'joinCourse.html', {'data': c})
        else:
            return redirect("/login/")



def joinCourse(request, course_id):
    if(request.method=="POST"):
        # course_id=request.session['course_id']
        newCourse=JoinedCourse(email=request.session["userID"],is_joined=True, joinedCourse=course_id)
        newCourse.save()
        a=Course.objects.filter(courseID=course_id)
        for x in a:
            return redirect("/subject/"+x.courseID+"/")

def compiler(request):
    if (request.method == "GET"):
        return render(request,'compiler.html')
    elif (request.method=="POST"):
        print(request.POST)
        # print(request.FILES)
        print(request.POST['source'])
        request.session['sourceCode']=request.POST['source']
        print(request.POST['codingLang'])
        request.session['codingLang']=request.POST['codingLang']
        print(request.session['codingLang'])
        request.session['input']=request.POST['input']
        if(request.POST['codingLang']=="Choose Coding Language"):
            if (request.POST['source'] == "Write your code here..."):
                return render(request, 'compiler.html',{'myerrormsg':'You have not written anything in the code section.'})
            else:
                return render(request, 'compiler.html',{'myerrormsg':'You have not selected any coding language.'})
        else:
            if (request.POST['source'] == "Write your code here..."):
                return render(request, 'compiler.html',{'myerrormsg':'You have not written anything in the code section.'})
            else:
                source=request.POST['source']
                input=request.POST['input']
                lan=request.POST['codingLang']
                if('compile' in request.POST):
                    m=MyCompiler()
                    compilation_msg=m.compile(source,lan)
                    print(compilation_msg)
                    cmsgs=compilation_msg
                    if (compilation_msg == "OK"):
                        cmsgs = ["Compiled Successfully",""]
                    else:
                        cmsgs = compilation_msg.split("\n")
                        if(len(cmsgs)>2):
                            cmsgs[2]=cmsgs[2].replace(" ","_")
                    # print(cmsgs)
                    return render(request, 'compiler.html',
                                  {'myCompilationMsg': cmsgs})
                elif('run' in request.POST):
                    m = MyCompiler()
                    compilation_msg,error = m.runCode(source, lan, input)
                    print(compilation_msg)
                    runmsgs=compilation_msg.split("\n")
                    if(error):
                        if(len(runmsgs)>2):
                            runmsgs[2]=runmsgs[2].replace(" ","_")
                    print(runmsgs)

                    return render(request, 'compiler.html',
                                  {'myRunMsg': runmsgs})


def yourCourses(request):
    if(request.method=="GET"):
        if(request.session['logged_in']):
            data2=[]
            data=JoinedCourse.objects.filter(email=request.session['userID'])
            for x in data:
                c=Course.objects.filter(courseID=x.joinedCourse)
                for y in c:
                    data2.append(y)
            return render(request, "yourCourses.html", {'yourCourses': data2})

def codingcomp(request):
    if(request.method=="GET"):
        if(request.session['logged_in']):
            com = CompQuestion.objects.filter(date_added=datetime.datetime.today())
            if(len(com)>0):
                for x in com:
                    comp = x
                    break
                r = CompResult.objects.filter(user=request.session['userID'])
                r1=r.filter(competitionQuestion=comp)
                print(len(r1))
                if(len(r1)==0):
                    testcases=CompQuesTestCase.objects.filter(competitionQuestion=comp)
                    m=0
                    sampletests=[]
                    for y in testcases:
                        sampletests.append(y)
                        if(m==1):
                            break
                        else:
                            m+=1

                    return render(request, 'codingcomp.html', {'testcases':testcases, 'comp':comp, 'sampletests':sampletests})
                else:
                    return render(request, 'alreadyresponded.html')
            else:
                return render(request, 'nocompetition.html')
        else:
            return redirect("/login/")
    elif (request.method=="POST"):
        com = CompQuestion.objects.filter(date_added=datetime.datetime.today())
        for x in com:
            comp = x
            break

        testcases = CompQuesTestCase.objects.filter(competitionQuestion=comp)
        m = 0
        sampletests = []
        for y in testcases:
            sampletests.append(y)
            if (m == 1):
                break
            else:
                m += 1
        print(request.POST)
        # print(request.FILES)
        print(request.POST['source'])
        request.session['sourceCode']=request.POST['source']
        print(request.POST['codingLang'])
        request.session['codingLang']=request.POST['codingLang']
        print(request.session['codingLang'])
        # request.session['input']=request.POST['input']
        if(request.POST['codingLang']=="Choose Coding Language"):
            if (request.POST['source'] == "Write your code here..."):
                return render(request, 'codingcomp.html',{'testcases':testcases, 'comp':comp, 'sampletests':sampletests, 'myerrormsg':'You have not written anything in the code section.'})
            else:
                return render(request, 'codingcomp.html',{'testcases':testcases, 'comp':comp, 'sampletests':sampletests, 'myerrormsg':'You have not selected any coding language.'})
        else:
            if (request.POST['source'] == "Write your code here..."):
                return render(request, 'codingcomp.html',{'testcases':testcases, 'comp':comp, 'sampletests':sampletests, 'myerrormsg':'You have not written anything in the code section.'})
            else:
                com = CompQuestion.objects.filter(date_added=datetime.datetime.today())
                for x in com:
                    comp = x
                    break

                testcases = CompQuesTestCase.objects.filter(competitionQuestion=comp)
                m = 0
                sampletests = []
                for y in testcases:
                    sampletests.append(y)
                    if (m == 1):
                        break
                    else:
                        m += 1
                source=request.POST['source']
                # input=request.POST['input']
                lan=request.POST['codingLang']
                if('compile' in request.POST):
                    m=MyCompiler()
                    compilation_msg=m.compile(source,lan)
                    print(compilation_msg)
                    cmsgs=compilation_msg
                    if (compilation_msg == "OK"):
                        cmsgs = ["Compiled Successfully",""]
                    else:
                        cmsgs = compilation_msg.split("\n")
                        if(len(cmsgs)>2):
                            cmsgs[2]=cmsgs[2].replace(" ","_")
                    # print(cmsgs)
                    return render(request, 'codingcomp.html',
                                  {'myCompilationMsg': cmsgs, 'testcases':testcases, 'comp':comp, 'sampletests':sampletests})
                elif('run' in request.POST):
                    m = MyCompiler()
                    results={}
                    for t in testcases:
                        compilation_msg,error = m.runCode(source, lan, t.input)
                        if(not error):
                            if(compilation_msg==t.output or compilation_msg==t.output+"\n" or compilation_msg+"\n"==t.output):
                                results[t.id]=True
                            else:
                                results[t.id]=False
                        else:
                            results[t.id]=False
                    # print(compilation_msg)
                    # runmsgs=compilation_msg.split("\n")
                    # if(error):
                    #     if(len(runmsgs)>2):
                    #         runmsgs[2]=runmsgs[2].replace(" ","_")
                    # print(runmsgs)

                    return render(request, 'codingcomp.html',
                                  {'results': results, 'testcases':testcases, 'comp':comp, 'sampletests':sampletests})
                elif ('submit' in request.POST):
                    m = MyCompiler()
                    results = []
                    for t in testcases:
                        compilation_msg, error = m.runCode(source, lan, t.input)
                        if (not error):
                            if (
                                    compilation_msg == t.output or compilation_msg == t.output + "\n" or compilation_msg + "\n" == t.output):
                                results.append(True)
                            else:
                                results.append(False)
                        else:
                            results.append(False)
                    passed=results.count(True)
                    result=(passed/len(testcases))*100
                    em = Email()
                    executor.submit(em.sendasubmitCompEmail(request, passed, result))
                    newResult=CompResult(competitionQuestion=comp, user=request.session['userID'], result=result, passed=passed)
                    newResult.save()
                    return render(request, "submitsuccess.html")

def compReview(request):
    new=CompQuestion.objects.filter(date_added=datetime.datetime.today())
    old=[]
    today=datetime.datetime.today()
    day=today.day
    month=today.month
    year=today.year
    for x in range(1, 6):
        day-=1
        yearst=str(year)
        if(day<10):
            dayst="0"+str(day)
        else:
            dayst=str(day)
        if(month<10):
            monthst="0"+str(month)
        else:
            monthst=str(month)
        c=CompQuestion.objects.filter(date_added=datetime.datetime.fromisoformat(str(yearst+"-" +monthst+ "-" +dayst)))
        for y in c:
            old.append(y)
    print(old)
    lengthold=len(old)
    lengthnew=len(new)
    return render(request, 'competitionreview.html',{'previous':old, 'new':new, 'lennew':lengthnew,'lenold':lengthold})


def accSettings(request):
    if(request.method=="GET"):
        if(request.session["logged_in"]):
            data=Account.objects.get(email=request.session['userID'])
            return render(request, 'accsettings.html', {'user':data})
        else:
            return redirect("/login/")

    elif(request.method=="POST"):
        if("updateImage" in request.POST):
            if("image" in request.FILES):
                image=request.FILES['image']
                # print(Account.objects.filter(email=request.session['userID']).update(image=image))
                data = Account.objects.get(email=request.session['userID'])
                data2 = NewUser.objects.get(email=request.session['userID'])
                data.image=image
                data2.image=image
                data.save()
                data2.save()
                return render(request, 'accsettings.html', {'user': data,
                                                            'imagesuccessrmsg': "Your profile image is updated successfully."})

            else:
                data = Account.objects.get(email=request.session['userID'])
                return render(request, 'accsettings.html', {'user': data, 'imageerrormsg':"You have not selected any image. Please select an image first."})

        if ("updateDetails" in request.POST):
            fname = request.POST['fname']
            lname = request.POST['lname']
            phone = request.POST['phone']
            data = Account.objects.get(email=request.session['userID'])
            data2 = NewUser.objects.get(email=request.session['userID'])
            detailerrormsg=[]
            detailsuccessmsg=[]
            if(fname!=""):
                if(validateName(fname)):
                    data.fname = fname
                    data2.fname = fname
                    request.session['userfName']=fname
                    data.save()
                    data2.save()
                    detailsuccessmsg.append("Your First Name is updated successfully.")
                else:
                    detailerrormsg.append("Entered first name is not valid. Please enter a valid first name.")
            if (lname != ""):
                if(validateName(lname)):
                    data.lname = lname
                    data2.lname = lname
                    data2.save()
                    data.save()
                    detailsuccessmsg.append("Your Last Name is updated successfully.")
                else:
                    detailerrormsg.append("Entered last name is not valid. Please enter a valid last name.")
            if (phone != ""):
                if(validatePN(phone)):
                    data.phone = phone
                    data2.phone = phone
                    data.save()
                    data2.save()
                    detailsuccessmsg.append("Your Phone Number is updated successfully.")
                else:
                    detailerrormsg.append("Entered phone number is not valid. Please enter a valid phone number.")
            return render(request, 'accsettings.html', {'user': data,
                                                        'detailerrormsg': detailerrormsg, 'detailsuccessmsg':detailsuccessmsg})

        if ("updatePassword" in request.POST):
            cpwd = request.POST['cpwd']
            npwd = request.POST['npwd']
            rpwd = request.POST['rpwd']
            data = Account.objects.get(email=request.session['userID'])
            data2 = NewUser.objects.get(email=request.session['userID'])
            passworderrormsg=""
            passwordsuccessmsg=""
            if(cpwd==data.password):
                if(npwd!="" and rpwd !=""):
                    if(npwd==rpwd):
                        data.password=npwd
                        data2.password=npwd
                        data2.save()
                        data.save()
                        passwordsuccessmsg="Your Password is updated successfully."
                        return render(request, 'accsettings.html', {'user': data,
                                                                    'passwordsuccessmsg':passwordsuccessmsg})
                    else:
                        passworderrormsg="Your new password and retype password did not match."
                        return render(request, 'accsettings.html', {'user': data,
                                                                    'passworderrormsg':passworderrormsg})
                else:
                    passworderrormsg = "Your new password and retype password can not be null."
                    return render(request, 'accsettings.html', {'user': data,
                                                                'passworderrormsg': passworderrormsg})
            else:
                passworderrormsg = "Your current password is not correct."
                return render(request, 'accsettings.html', {'user': data,
                                                            'passworderrormsg': passworderrormsg})


def joinedcomps(request):
    new = CompQuestion.objects.filter(date_added=datetime.datetime.today())
    old = []
    today = datetime.datetime.today()
    day = today.day
    month = today.month
    year = today.year
    for x in range(1, 6):
        day -= 1

        yearst = str(year)
        if (day < 10):
            dayst = "0" + str(day)
        else:
            dayst = str(day)
        if (month < 10):
            monthst = "0" + str(month)
        else:
            monthst = str(month)
        c = CompQuestion.objects.filter(
            date_added=datetime.datetime.fromisoformat(str(yearst + "-" + monthst + "-" + dayst)))
        for y in c:
            old.append(y)
    print(old)
    lengthold = len(old)
    lengthnew = len(new)
    joinedcomps=CompResult.objects.filter(user=request.session['userID'])
    return render(request, 'joinedcomps.html',
                  {'previous': old, 'new': new, "joinedcomps":joinedcomps, 'lenjc':len(joinedcomps), 'lennew': lengthnew, 'lenold': lengthold, })


def tests(request):
    new = WeekTest.objects.filter(date_added=datetime.datetime.today())
    old = []
    up = WeekTest.objects.filter(date_added__gt=datetime.datetime.today())
    today = datetime.datetime.today()
    day = today.day
    month = today.month
    year = today.year
    for x in range(1,40):
        day -= 1
        if(day==0):
            day+=30
            if(month==1):
                month=12
                year-=1
            else:
                month-=1


        yearst = str(year)
        if (day < 10):
            dayst = "0" + str(day)
        else:
            dayst = str(day)
        if (month < 10):
            monthst = "0" + str(month)
        else:
            monthst = str(month)
        c = WeekTest.objects.filter(
            date_added=datetime.datetime.fromisoformat(str(yearst + "-" + monthst + "-" + dayst)))
        for y in c:
            old.append(y)
    print(old)
    lengthold = len(old)
    lengthnew = len(new)
    return render(request, 'weeklytestreview.html', {'lengthnew':lengthnew,'upcoming':up, 'lengthup':len(up), 'lengthold':lengthold, 'new':new, 'old':old })

def takeTest(request, test_id):
    if(request.session['logged_in']):
        try:
            test=WeekTest.objects.get(test_id=test_id)
            wr = WeekTestResult.objects.filter(test=test, user=request.session['userID'])
            if(len(wr)==0):
                j=JoinedCourse.objects.filter(email=request.session['userID'], joinedCourse=test.course.courseID)
                if(len(j)>0):
                    return render(request, 'teststartreview.html', {'test':test})
                else:

                    new = WeekTest.objects.filter(date_added=datetime.datetime.today())
                    old = []
                    up = WeekTest.objects.filter(date_added__gt=datetime.datetime.today())
                    today = datetime.datetime.today()
                    day = today.day
                    month = today.month
                    year = today.year
                    for x in range(1, 40):
                        day -= 1
                        if (day == 0):
                            day += 30
                            if (month == 1):
                                month = 12
                                year -= 1
                            else:
                                month -= 1

                        yearst = str(year)
                        if (day < 10):
                            dayst = "0" + str(day)
                        else:
                            dayst = str(day)
                        if (month < 10):
                            monthst = "0" + str(month)
                        else:
                            monthst = str(month)
                        c = WeekTest.objects.filter(
                            date_added=datetime.datetime.fromisoformat(str(yearst + "-" + monthst + "-" + dayst)))
                        for y in c:
                            old.append(y)
                    print(old)
                    lengthold = len(old)
                    lengthnew = len(new)
                    return render(request, 'weeklytestreview.html',
                                  {'lengthnew': lengthnew, 'lengthold': lengthold,'upcoming':up, 'lengthup':len(up), 'new': new, 'old': old,
                                   'errormsg': "You have not joined "+test.course.courseName+" Course. Go to courses and join for the course first."})
            else:
                return render(request, 'submittedalready.html')
        except:
            new = WeekTest.objects.filter(date_added=datetime.datetime.today())
            up = WeekTest.objects.filter(date_added__gt=datetime.datetime.today())
            old = []
            today = datetime.datetime.today()
            day = today.day
            month = today.month
            year = today.year
            for x in range(1, 40):
                day -= 1
                if (day == 0):
                    day += 30
                    if (month == 1):
                        month = 12
                        year -= 1
                    else:
                        month -= 1

                yearst = str(year)
                if (day < 10):
                    dayst = "0" + str(day)
                else:
                    dayst = str(day)
                if (month < 10):
                    monthst = "0" + str(month)
                else:
                    monthst = str(month)
                c = WeekTest.objects.filter(
                    date_added=datetime.datetime.fromisoformat(str(yearst + "-" + monthst + "-" + dayst)))
                for y in c:
                    old.append(y)
            print(old)
            lengthold = len(old)
            lengthnew = len(new)
            print(up)
            return render(request, 'weeklytestreview.html',
                          {'lengthnew': lengthnew, 'lengthold': lengthold, 'new': new,'upcoming':up, 'lengthup':len(up),'old': old, 'errormsg':"The test is not valid anymore."})
    else:
        return redirect("/login/")


def startTest(request, test_id):
    if(request.method=="GET"):
        test=WeekTest.objects.get(test_id=test_id)
        questions=WeekTestQuestion.objects.filter(test=test)
        print(questions)
        return render(request, "maintest.html",
                      {'test':test,
                       'questions':questions})
    elif(request.method=="POST"):
        marks=0
        print(request.POST)
        test = WeekTest.objects.get(test_id=test_id)
        questions = WeekTestQuestion.objects.filter(test=test)
        print(questions)
        for x in questions:
            if(x.question_id in request.POST):
                if(x.answer=="A"):
                    ans="option1"
                elif(x.answer=="B"):
                    ans="option2"
                elif(x.answer=="C"):
                    ans="option3"
                elif(x.answer=="D"):
                    ans="option4"
                if(request.POST[x.question_id]==ans):
                    marks+=1
        result=(marks/len(questions))*100
        em=Email()
        executor.submit(em.sendasubmitTestEmail(request, marks, result))
        a=WeekTestResult(test=test, user=request.session['userID'],
                         result=result, marks=marks)
        a.save()
        return render(request, "submitsuccess.html")

def testScores(request):
    testResults=WeekTestResult.objects.filter(user=request.session['userID'])
    return render(request,'testscores.html',{'lenres':len(testResults),'testResults':testResults})

def yourTests(request):
    try:
        data = Account.objects.get(email=request.session['userID'])
        joinedCourse = JoinedCourse.objects.filter(email=data.email)
        testData = []
        oldtestData = []
        for x in joinedCourse:
            oldtest = WeekTest.objects.filter(course__courseID=x.joinedCourse, date_added__lt=datetime.datetime.today())
            print(oldtest)
            for y in oldtest:
                oldtestData.append(y)
            try:
                test = WeekTest.objects.get(course__courseID=x.joinedCourse, date_added=datetime.datetime.today())
                print(test)
                testData.append(test)
            except:
                pass
        return render(request, 'yourtests.html', {'lentestData':len(testData), 'testData':testData, 'lenoldtestData':len(oldtestData), 'oldtestData':oldtestData})
    except:
        return redirect('/dashboard/')


def feedback(request):
    if(request.method=="GET"):
        return render(request, 'feedback.html')
    elif(request.method=="POST"):
        a=len(Feedback.objects.all())
        f=Feedback(feedback_id=request.session['userID']+"_feed_"+str(a+1) , test_comp=request.POST['test'], study_materials=request.POST['study'], compiler=request.POST['compiler'], overall=request.POST['overall'], suggestion=request.POST['suggestion'], comment=request.POST['comment'], rating=request.POST['rating'])
        f.save()
        return render(request, 'feedback.html')

def contactus(request):
    return render(request, 'contactus.html')
