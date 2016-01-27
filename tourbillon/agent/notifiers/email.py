# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText


class EmailNotifier(object):
    """docstring for ClassName"""

    def __init__(self, **kwargs):
        super(EmailNotifier, self).__init__()
        self._from = kwargs.get('from', None)
        self._to = kwargs.get('to', None)
        self._cc = kwargs.get('cc', None)
        self._bcc = kwargs.get('bcc', None)
        self._host = kwargs.get('host', 'localhost')
        self._port = kwargs.get('port', 25)
        self._username = kwargs.get('username')
        self._password = kwargs.get('password')
        self._use_tls = kwargs.get('use_tls', False)

        self._validate()

    def _validate(self):
        if not self._from:
            raise Exception('"from" is required')
        if not any([self._to, self._cc, self._bcc]):
            raise Exception('at least one of "to", "cc" or "bcc" is required')

    def connect(self):
        pass

    def disconnect(self):
        pass

    def notify(self):
        pass
