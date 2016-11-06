import os
from tarhosting.app import app


DEV_LISTEN_HOST = os.getenv('DEV_LISTEN_HOST', '127.0.0.1')
DEV_LISTEN_PORT = int(os.getenv('DEV_LISTEN_PORT', '5000'))


def main():
    print app
    app.debug = True
    app.run(DEV_LISTEN_HOST, DEV_LISTEN_PORT)


if __name__ == '__main__':
    main()
