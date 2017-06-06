# coding:utf8

from mutils.phemail import send_email
from celery import task

@task
def sendmail(simple_url,email,check_url,check_data=None,subject=None,message=None):
    try:
        print '==' * 20
        print 'send_mail'
        print '==' * 20
        send_email(simple_url,email,check_url,check_data,subject,message)
    except Exception:
        return False

    return True
