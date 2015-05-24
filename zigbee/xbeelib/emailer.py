from time import time
import smtplib
class Emailer(object):
    def __init__(self):
        self.now = None
        self.tolist = ("manjinder.bains@gmail.com", "bains.beant@gmail.com")
    def sendMail(self, timestamp, subject, message, critical = False):
        if critical:
            self.now = None
        if self.now is None or (time() - self.now > 200):
            mail = smtplib.SMTP("localhost")
            self.now = time()
            try:
                msg = ("Subject: %s\n" 
                    "\n  At %s\n"
                    "\n  Message/Count: %s") % (subject, timestamp, message)
                mail.sendmail("1169ashford@lincoln.com", self.tolist, msg)
                print "Email sent:\n", msg
            except Exception, e:
                print "MAIL ERROR", Exception, e
            mail.close()

