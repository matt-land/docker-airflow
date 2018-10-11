import os
import pypd
import socket
import json
import logging
from airflow.utils import timezone


class PagerDuty(object):

    SEVERITY_WARNING = 'warning'
    SEVERITY_ERROR = 'error'
    SEVERITY_NOTICE = 'notice'
    SEVERITY_INFO = 'info'

    ROUTING_KEY = os.environ.get('PAGERDUTY_ROUTING_KEY')

    def __init__(self, message, severity=SEVERITY_WARNING, payload=None, error_class=None):
        # type (str, str, dict, str) -> None
        self._message = message
        self._send_reasons = []
        self._response = None
        self._has_sent = False

        self._data = {
            'routing_key': self.ROUTING_KEY,
            'event_action': 'trigger',
            'payload': {
               'summary': self.message,
               'severity': severity,
               'source': socket.gethostname(),
               'timestamp': timezone.utcnow().isoformat(),
               'class': error_class,
               'payload': json.dumps(payload)
            }
        }

    @property
    def message(self):
        return self._message[:512]

    @property
    def response(self):
        return self._response

    @property
    def send_reasons(self):
        return self._send_reasons

    @property
    def has_sent(self):
        return self._has_sent

    def _should_send(self):
        self._send_reasons = []
        if self.has_sent:
            self._send_reasons.append('already sent')
        return len(self._send_reasons) == 0

    def send(self):
        # the automated test relies on this- don't

        if not self._should_send():
            logging.info('{} triggered but not sent: {} '.format(self.__class__.__name__, ', '.join(self.send_reasons)))
            logging.info(self.message)
            self._has_sent = True  # don't move
            return False
        logging.info('{} triggered: {} '.format(self.__class__.__name__, self.message))
        self._has_sent = True  # don't move
        self._send()
        return True

    def _send(self):
        self._response = pypd.EventV2.create(data=self._data)
