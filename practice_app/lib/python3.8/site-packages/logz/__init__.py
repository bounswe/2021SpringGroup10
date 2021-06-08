"""日志配置"""
import re
import os
import io
import json
from datetime import datetime
import time
import inspect
from collections import defaultdict
import logging
import smtplib
from email.mime.text import MIMEText
from logging import addLevelName, currentframe
import traceback
import threading
from functools import wraps
from logging.handlers import BaseRotatingHandler

LOG_ITEMS = ('name', 'levelno', 'levelname', 'pathname', 'filename', 'funcName',
             'lineno', 'asctime', 'thread', 'threadName', 'process', 'message')


LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'

LOG_LEVEL_MAP = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'warn': logging.WARN,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}


class DayRotatingHandler(BaseRotatingHandler):
    def __init__(self, filename, mode, encoding=None, delay=False):
        self.filename = filename
        self.date = datetime.now().date()
        super().__init__(filename, mode, encoding, delay)

    def shouldRollover(self, record):
        return self.date != datetime.now().date()

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.baseFilename = self.date.strftime(self.filename)
        self._open()


class BufferingSMTPHandler(logging.handlers.BufferingHandler):
    def __init__(self, host, user, password, receivers: list, subject, capacity, port=None, sender=None, ssl=True):
        logging.handlers.BufferingHandler.__init__(self, capacity)
        self.host = host
        self.port = port
        self.ssl = ssl
        self.user = user
        self.password = password
        self.subject = subject
        self.sender = sender or user
        self.receivers = receivers if isinstance(receivers, list) else [receivers]

    def send_email(self):
        smtp = smtplib.SMTP_SSL(self.host, self.port) if self.ssl else smtplib.SMTP(self.host, self.port)
        body = ''
        for record in self.buffer:
            s = self.format(record)
            body += s + "\r\n"

        msg = MIMEText(body, 'plain', 'utf-8')
        msg['from'] = self.sender
        msg['to'] = ','.join(self.receivers)
        msg['subject'] = self.subject
        smtp.login(self.user, self.password)
        for receiver in self.receivers:
            smtp.sendmail(self.sender, receiver, msg.as_string())

    def flush(self):
        if len(self.buffer) > 0:
            self.send_email()
            self.buffer = []


class HTMLHandler(logging.FileHandler):
    pass


class Logger(logging.Logger):
    """Rewrite findCaller to show the real funcName"""
    def findCaller(self, stack_info=False):
        _srcfile = os.path.normcase(addLevelName.__code__.co_filename)
        f = currentframe()
        if f is not None:
            f = f.f_back
            try:
                f = getattr(f.f_back, 'f_back', None)
            except:
                pass
            rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                try:
                    f = getattr(f.f_back, 'f_back', None)
                except:
                    pass
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv


class DecoLogger(logging.Logger):
    """Rewrite findCaller to show the real funcName for logit decorator"""
    def findCaller(self, stack_info=False):
        _srcfile = os.path.normcase(addLevelName.__code__.co_filename)
        f = currentframe()
        if f is not None:
            f = f.f_back
            try:
                f = getattr(f.f_back, 'f_back', None)
                f = getattr(f.f_back, 'f_back', None)
            except:
                pass
            rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                try:
                    f = getattr(f.f_back, 'f_back', None)
                    f = getattr(f.f_back, 'f_back', None)
                except:
                    pass
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv


class Log(object):
    def __init__(self, name=__name__, logger_class=None):
        self.name = name
        # self.__logger = logging.getLogger(name)
        logger_class = logger_class or Logger
        self.__logger = logger_class(name)
        self.__format = logging.Formatter(LOG_FORMAT)
        self.__level = logging.DEBUG
        self.__extra = None
        self.__file = None
        self.__email = None

        self.verbosity = None
        self.filter = None
        self.hook = None  # todo
        self.html = None
        self.db = None
        self.server = None

        self.outputs = defaultdict(str)

        ch = logging.StreamHandler()
        ch.setFormatter(self.__format)

        self.__logger.setLevel(self.__level)
        self.__logger.addHandler(ch)

    @property
    def level(self):
        return self.__level

    def _parse_level(self, value):
        if isinstance(value, int) and value in (0,10,20,30,40,50):
            return value
        if isinstance(value, str):
            value = value.lower()
            return LOG_LEVEL_MAP.get(value, logging.DEBUG)

    @level.setter
    def level(self, value):
        self.__level = self._parse_level(value)
        self.__logger.setLevel(self.__level)

    @property
    def format(self):
        return self.__format

    @format.setter
    def format(self, value):
        items = re.findall(r'%\((.*?)\)s', value)
        self.__extra = {key: None for key in (set(items)-set(LOG_ITEMS))}
        self.__format = logging.Formatter(value)

        for handler in self.__logger.handlers:
            handler.setFormatter(self.__format)

    @property
    def file(self):
        return self.__file

    @file.setter
    def file(self, value):  # todo
        if '%' in value:
            value = datetime.now().strftime(value)
            fh = DayRotatingHandler(value, 'a', encoding='utf-8')
        else:
            # fh = logging.handlers.RotatingFileHandler(value, 'a', encoding='utf-8', maxBytes=10240, backupCount=5)
            fh = logging.FileHandler(value, 'a', encoding='utf-8')
        fh.setFormatter(self.__format)
        self.__file = value
        self.__logger.addHandler(fh)

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value
        host = value.get('host')
        port = value.get('port')
        ssl = value.get('ssl')
        user = value.get('user')
        password = value.get('password')
        sender = value.get('sender') or user
        receivers = value.get('receivers')
        capacity = value.get('capacity', 10)
        subject = value.get('subject', '[logz]log message')
        level = value.get('level')

        log_level = self._parse_level(level) if level else logging.ERROR
        # eh = logging.handlers.SMTPHandler(host, sender, receivers, subject, credentials=(user, password), secure=())
        eh = BufferingSMTPHandler(host, user, password, receivers, subject, capacity, port, sender, ssl)
        eh.setLevel(log_level)
        eh.setFormatter(self.__format)
        self.__logger.addHandler(eh)

    @property
    def logger(self):
        return self.__logger

    def log(self, level, msg, *args, **kwargs):
        if args:
            msg = '%s %s' % (str(msg), ' '.join([str(arg) for arg in args]))
        if self.__extra:
            extra = kwargs.get('extra', {})
            kwargs['extra'] = self.__extra
            kwargs['extra'].update(extra)

        if 'indent' in kwargs:  # todo
            indent = kwargs.pop('indent')
            if indent and isinstance(msg, dict):
                msg = '->\n' + json.dumps(msg, indent=indent, ensure_ascii=False)

        if level == 'critical':
            self.__logger.critical(msg, **kwargs)
        elif level == 'error':
            self.__logger.error(msg, **kwargs)
        elif level == 'exception':
            self.__logger.exception(msg, **kwargs)
        elif level == 'warning':
            self.__logger.warning(msg, **kwargs)
        elif level == 'info':
            self.__logger.info(msg, **kwargs)
        else:
            self.__logger.debug(msg, **kwargs)

    def print(self, msg, *args, **kwargs):
        thread_id = str(threading.current_thread().ident)
        if args:
            msg = '%s %s' % (str(msg), ' '.join([str(arg) for arg in args]))
        self.outputs[thread_id] += str(msg)
        self.log('info', msg, *args, **kwargs)

    def get_output(self):
        thread_id = str(threading.current_thread().ident)
        return self.outputs[thread_id]

    def debug(self, msg, *args, **kwargs):
        self.log('debug', msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log('info', msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.log('warning', msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.log('warning', msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log('error', msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.log('exception', msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.log('critical', msg, *args, **kwargs)


log = Log()


def _to_string(args, kwargs):
    params = []
    for arg in args:
        params.append(str(arg))
    for k, v in kwargs.items():
        params.append(f'{k}={v}')
    return ','.join(params)


def logit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        parent_action = inspect.stack()[1][3].strip()
        log = Log(logger_class=DecoLogger)
        # log.format = '%(asctime)s %(levelname)s %(name)s %(filename)s [%(funcName)s] %(lineno)d %(message)s'
        result = func(*args, **kwargs)
        log.debug(f"{parent_action} -> {func.__name__}({_to_string(args, kwargs)}) return: {result} "
                 f"duration: {time.time() - start}s")

        return result
    return wrapper

if __name__ == '__main__':
    log.format = '%(asctime)s %(levelname)s %(user)s %(message)s'
    log.info('hello with no user')
    log.info('hello with kevin', extra={'user': 'kevin'})
