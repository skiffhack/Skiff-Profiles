# Copy this file to settings/secrets.py
#
# Put secrets in here. SECRET_KEY, API keys, SMTP server passwords,
# anything you don't want in version control.
#
# For convenience, you can run `python settings/secrets_template.py` and
# then copy-and-paste the generated key into your secrets.py file.

SECRET_KEY = 'complete_this'

if __name__ == '__main__':
    from random import choice
    print ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
