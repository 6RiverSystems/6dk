from threading import Thread

from flask_mail import Message
from flask import render_template

from app import app, mail
from app.models import Profile, User


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, recipients, text_body, html_body,
              sender=app.config['MAIL_USERNAME'], attachments=[]):
    msg = Message(
        subject,
        sender=app.config['MAIL_USERNAME'],
        recipients=recipients,
        body=text_body
    )
    msg.body = text_body
    msg.email = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_welcome(user, temp_pass):
    send_mail('[6DK - 6 River Systems] Welcome',
              recipients=[user.email],
              text_body=render_template('email/welcome.txt',
                                        user=user, temp_pass=temp_pass),
              html_body=render_template('email/welcome.html',
                                        user=user, temp_pass=temp_pass))


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_mail('[6DK - 6 River Systems] Reset Your Password',
              recipients=[user.email],
              text_body=render_template('email/reset_password.txt',
                                        user=user, token=token),
              html_body=render_template('email/reset_password.html',
                                        user=user, token=token))


def send_password_reset_done_email(user):
    token = user.get_reset_password_token()
    send_mail('[6DK - 6 River Systems] Your Password Has Been Reset',
              recipients=[user.email],
              text_body=render_template('email/reset_password_done.txt',
                                        user=user, token=token),
              html_body=render_template('email/reset_password_done.html',
                                        user=user, token=token))


def send_forward_profile_email(current_user, recipient, token):
    jwt_token = current_user.get_forward_profile_token(recipient, token)
    profile = Profile.query.filter_by(token_id=token).first().to_dict()
    send_mail('[6DK - 6 River Systems] You Received a New Profile',
              recipients=[recipient.email],
              text_body=render_template('email/send_profile.txt',
                                        sender=current_user,
                                        user=recipient, jwt_token=jwt_token,
                                        profile=profile),
              html_body=render_template('email/send_profile.html',
                                        sender=current_user,
                                        user=recipient, jwt_token=jwt_token,
                                        profile=profile))


def send_accept_profile_email(source_id, recipient, token):
    source = User.query.filter_by(id=source_id).first()
    profile = Profile.query.filter_by(token_id=token).first().to_dict()
    send_mail('[6DK - 6 River Systems] Your Profile Was Accepted',
              recipients=[source.email],
              text_body=render_template('email/accept_profile.txt',
                                        source=source, recipient=recipient,
                                        profile=profile),
              html_body=render_template('email/accept_profile.html',
                                        source=source, recipient=recipient,
                                        profile=profile))
