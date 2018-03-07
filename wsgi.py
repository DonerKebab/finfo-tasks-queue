# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    admin wsgi module
"""

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from admin import data as data

data_app = data.create_app()
application = DispatcherMiddleware(data_app, {})


if __name__ == '__main__':
    run_simple('0.0.0.0', 8000, application, use_reloader=True, use_debugger=True)
