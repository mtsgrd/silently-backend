# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()
from silently.manage import manager

if __name__ == "__main__":
    manager.run()
