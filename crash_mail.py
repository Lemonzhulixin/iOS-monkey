#!/usr/bin/python
#-*-coding:utf-8-*-
import smtplib
import os
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

#邮件配置
MAIL_FROM_ADDRESS = "xxxx@quvideo.com"
MAIL_PASSWORD = "xxxxxx"
SMTP_SERVER = "smtp.exmail.qq.com"

#接收邮件的邮箱
MAIL_TO_ADDRESS_APPSTORE = ['lixin.zhu@quvideo.com']

#发送邮件
#mail_info包含：mail_subject, mail_message
def send_Email(mail_info, receiver):
    
    print ('*******开始发送邮件****')
    
    #邮件接受者
    mail_receiver = receiver

    #根据不同邮箱配置 host，user，和pwd
    mail_host = SMTP_SERVER
    mail_port = 465
    mail_user = MAIL_FROM_ADDRESS
    mail_pwd = MAIL_PASSWORD
    
    mail_to = ','.join(mail_receiver)

    msg = MIMEMultipart()

    #文本内容
    message = mail_info['mail_message']
    subject = mail_info['mail_subject']
    body = MIMEText(message, _subtype='html', _charset='utf-8')
    msg.attach(body)

    # 文件类型的附件
    appendix = mail_info['mail_file']
    if len(appendix) > 0:
        
        filename = os.path.basename(appendix)
        filepart = MIMEApplication(open(appendix, 'rb').read())
        filepart.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(filepart)


    msg['To'] = mail_to
    msg['from'] = mail_user
    msg['subject'] = subject
    
    try:
        s = smtplib.SMTP()
        # 设置为调试模式，就是在会话过程中会有输出信息
        s.set_debuglevel(1)
        s.connect(mail_host)
        s.login(mail_user, mail_pwd)
        s.sendmail(mail_user, mail_receiver, msg.as_string())
        s.close()
        
        print ('*******邮件发送成功*******')
    except Exception as e:
        print(e)

def send_Email_to_developer(mail_info):
    send_Email(mail_info, MAIL_TO_ADDRESS_APPSTORE)

def main():
    print("auto_email")

    if len(sys.argv) > 2:

        #邮件类型 测试成功 测试失败
        fuction_type = sys.argv[1]
        #邮寄的title
        subject = sys.argv[2]
        #邮寄的内容
        message = sys.argv[3]
        #邮件附件
        if len(sys.argv) > 4:
            appendix = sys.argv[4]
        else:
            appendix = ''

        if fuction_type == "fail":

            mail_info = {
                    'mail_subject' : subject,
                    'mail_message' : message,
                    'mail_file' : appendix,
                    }

            send_Email_to_developer(mail_info)

            print("-------------测试出现Crash-------------")

        elif fuction_type == "success":

            mail_info = {
                    'mail_subject' : subject,
                    'mail_message' : message
                }
            send_Email_to_developer(mail_info)

            print("-------------success-------------")
        else:
            print("Fail operation", fuction_type)
    else:
        print("Fail operation")

# 执行
main()

