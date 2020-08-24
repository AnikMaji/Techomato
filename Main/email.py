from .decode import Decode
import smtplib
from . import views
from email.message import EmailMessage


class Email:

    def sendaEmail(self):

        global email
        obj=Decode()
        pwd=obj.funcDecode(b'gAAAAABetnY87Y--hKREey7_cOAg-bQNDyuyCJioK8owaLx4RRGZXocSF8kH80MIgsPwXcWIGM84Vcd8JDhvrvOAQBH1eZntUQ==')
        sender = 'techomato.server@gmail.com'
        message = """From: TechOmato <techomato.server@gmail.com>
To: Person
MIME-Version: 1.0
Content-type: text/html
Subject: Registration Successful

<h1>Your account has been successfully created.</h1>
<b1><b>Please log in to your account.</b></b2>
"""
        msg = EmailMessage()
        msg.add_header("Header","This is the header")
        msg.set_content('This is my message')
        msg['Subject'] = 'Registration Successful'
        msg['From'] = sender
        msg['To'] = views.email

        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com',587)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.ehlo()
            smtpObj.login(sender, pwd)
            smtpObj.sendmail(sender, views.email, message)
            # smtpObj.sendmail()
            print("Successfully sent email")
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print(e)




    def sendOTP(self, otp):

        global email
        obj=Decode()
        #pwd=obj.funcDecode(b'gAAAAABetnY87Y--hKREey7_cOAg-bQNDyuyCJioK8owaLx4RRGZXocSF8kH80MIgsPwXcWIGM84Vcd8JDhvrvOAQBH1eZntUQ==')
        pwd="server@007"
        sender = 'techomato.server@gmail.com'

        print(otp)
        message = """From: TechOmato <techomato.server@gmail.com>
To: {}
MIME-Version: 1.0
Content-type: text/html
Subject: Verify Your Email

<h1>You are just one step ahead to complete registration process with us.</h1>
<b1><b>Your secret password is {}. Please log in to your account to activate.</b></b2>
""".format(views.email,str(otp))
        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com',587)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.ehlo()
            smtpObj.login(sender, pwd)
            smtpObj.sendmail(sender, views.email, message)
            # smtpObj.sendmail()
            print("Successfully sent email")
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print(e)
    def generate_otp(self):
        import random
        otp = 0
        for i in range(6):
            a = random.randint(1, 9)
            otp = otp * 10 + a
        return otp

    def sendSuccessEmail(self, successEmail):

        global email
        obj=Decode()
        #pwd=obj.funcDecode(b'gAAAAABetnY87Y--hKREey7_cOAg-bQNDyuyCJioK8owaLx4RRGZXocSF8kH80MIgsPwXcWIGM84Vcd8JDhvrvOAQBH1eZntUQ==')
        pwd="server@007"
        sender = 'techomato.server@gmail.com'
        message = """From: TechOmato <techomato.server@gmail.com>
To: {}
MIME-Version: 1.0
Content-type: text/html
Subject: Registration Successful

<h1>Your account has been successfully created.</h1>
<b1><b>You can now log in to your account and start learning with us.</b></b2>
""".format(successEmail)

        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com',587)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.ehlo()
            smtpObj.login(sender, pwd)
            smtpObj.sendmail(sender, successEmail, message)
            # smtpObj.sendmail()
            print("Successfully sent email")
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print(e)

    def sendasubmitTestEmail(self,request, marks, result):
        obj = Decode()
        #pwd=obj.funcDecode(b'gAAAAABetnY87Y--hKREey7_cOAg-bQNDyuyCJioK8owaLx4RRGZXocSF8kH80MIgsPwXcWIGM84Vcd8JDhvrvOAQBH1eZntUQ==')
        pwd="server@007"
        sender = 'techomato.server@gmail.com'
        message = """From: TechOmato <techomato.server@gmail.com>
To: {}
MIME-Version: 1.0
Content-type: text/html
Subject: Submission Complete

<h1>Your answers have been successfully submitted.</h1>
<h4>You got {} marks.</h4>
<h4>You got {}% marks.</h4>
<b1><b>You can now log in to your account and start learning with us.</b></b2>
""".format(request.session['userID'], marks, result)


        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.ehlo()
            smtpObj.login(sender, pwd)
            smtpObj.sendmail(sender, request.session['userID'], message)
            print("Successfully sent email")
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print(e)
    def sendasubmitCompEmail(self,request, passed, result):
        obj = Decode()
       #pwd=obj.funcDecode(b'gAAAAABetnY87Y--hKREey7_cOAg-bQNDyuyCJioK8owaLx4RRGZXocSF8kH80MIgsPwXcWIGM84Vcd8JDhvrvOAQBH1eZntUQ==')
        pwd="server@007"
        sender = 'techomato.server@gmail.com'
        message = """From: TechOmato <techomato.server@gmail.com>
To: {}
MIME-Version: 1.0
Content-type: text/html
Subject: Submission Complete

<h1>Your answers have been successfully submitted.</h1>
<h4>Your code passed {} test cases.</h4>
<h4>You got {}% marks.</h4>
<b1><b>You can now log in to your account and start learning with us.</b></b2>
""".format(request.session['userID'], passed, result)

        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.ehlo()
            smtpObj.login(sender, pwd)
            smtpObj.sendmail(sender, request.session['userID'], message)
            print("Successfully sent email")
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print(e)
