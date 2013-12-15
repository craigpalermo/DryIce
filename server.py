import sys

from flask         import Flask
from datetime      import datetime
from time          import sleep
from threading     import Thread

from fileutils    import expire_files

app = Flask(__name__)

def main():
    datetime.strptime('2013-01-01', '%Y-%m-%d')

    expire_files_thread = Thread(
            target=expire_files)
    #flask_server_thread  = Thread(
    #        target=lambda: app.run(host='0.0.0.0', debug=True))

    expire_files_thread.daemon = True
    #flask_server_thread.daemon  = True

    expire_files_thread.start()
    #flask_server_thread.start()

    app.run(host='0.0.0.0', debug=True)

    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            sys.exit()


if __name__ == "__main__":
    main()
