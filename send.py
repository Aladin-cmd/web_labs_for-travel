import smtplib

gmail_user = 'testmail1234ttt@gmail.com'
gmail_password = 'qw12as12zx'


def send_email(to_receive, subjectText, text, sender, ps):
    sent_from = sender
    to = to_receive
    subject = subjectText
    body = text

    email_text = """\
    From: %s
    To: %s
    \nSubject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(sender, ps)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong….", ex)
