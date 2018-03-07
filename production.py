# -*- coding: utf-8 -*-
"""
    production
    ~~~~

    admin production module
"""

from admin import data
import logging

app = data.create_app()
app.logger.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
