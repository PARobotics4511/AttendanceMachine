import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import datetime
import calendar
from datetime import date

def check_send():
    print("about to send log")
    with open("/home/pi/Documents/AttendanceMachine/sent_log.txt","r") as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
        print last_line
        if str(datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d').strftime('%m-%d-%y')) not in last_line and datetime.datetime.now().time() >= datetime.time(16,00):
            print("We're gonna send this one, my man")
            ammended_file = open("/home/pi/Documents/AttendanceMachine/sent_log.txt","a")
            ammended_file.write("\n" + str(datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d').strftime('%m-%d-%y')) + " : Sent!")
            send()
        else:
            print("it's not time to send it yet!")
def send():
    fromaddr = "frc4511attendancebot@gmail.com"
    toaddr = "michael.plucinski@providenceacademy.org"
    #toaddr = "luke.igel@gmail.com"
     
    msg = MIMEMultipart()

    my_date = date.today()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "FRC 2018 Attendance Log - " + str(calendar.day_name[my_date.weekday()]) + ", " + str(datetime.date.today())


    body = "Here's the log from " + str(calendar.day_name[my_date.weekday()]) + ", " + str(datetime.date.today()) + " !"

     
    msg.attach(MIMEText(body, 'plain'))
     
    filename = "log-" + datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d').strftime('%m-%d-%y') + ".csv"
    attachment = open("logs/log-" + datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d').strftime('%m-%d-%y') + ".csv", "rb")
     
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
     
    msg.attach(part)
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "PARobotics4511")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print("Email sent, hopefully!")
