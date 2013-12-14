import threading
import time
import sys

from   bottle        import run
from   datetime      import datetime

from   lib.fileutils import expire_files


def main():
    datetime.strptime('2013-01-01', '%Y-%m-%d')

    expire_files_thread = threading.Thread(
            target=expire_files)
    main_bottle_thread  = threading.Thread(
            target=lambda: run(host='0.0.0.0', port=8080, debug=True))

    expire_files_thread.daemon = True
    main_bottle_thread.daemon  = True

    expire_files_thread.start()
    main_bottle_thread.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit()


if __name__ == "__main__":
    main()
