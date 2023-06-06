#!/usr/bin/env python3
from util import listen
from service import main
while True:
    try:
        listen(main)
    except Exception as e:
        log(str(e))
