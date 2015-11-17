__author__ = 'tobias'

import logging


class Web:

    def __init__(self):
        logging.info("init web")

    @staticmethod
    def update(date, temp, pid):
        f1 = open('/var/www/index.php', 'w+')

        f1.write("<html>")
        f1.write("<head></head>")
        f1.write("<body><h1>Incubator</h1>")

        f1.write("<div class='date'>")
        f1.write(str(date))
        f1.write("</div>")

        f1.write("<div class='temp'>")
        f1.write(str(temp))
        f1.write("</div>")

        f1.write("<div class='pid'>")
        f1.write(str(pid))
        f1.write("</div>")

        f1.write("<div class='stop'></div>")

        f1.write("</body>")
