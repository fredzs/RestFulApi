from app import create_app
app = create_app('default')
import sys


if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000
    app.run(port=port, ssl_context=("ssl/www.fredirox.com.crt", "ssl/www.fredirox.com.key"))
