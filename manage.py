from app import create_app
import sys, getopt
from Config import GLOBAL_CONFIG
app = create_app('default')


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["mode=", "port="])
    port = 5000
    for opt in opts:
        if opt[0] == "--port":
            port = int(opt[1])
        if opt[0] == "--mode":
            GLOBAL_CONFIG.set_field("Setting", "mode", opt[1])
    app.run(port=port, ssl_context=("ssl/www.fredirox.com.crt", "ssl/www.fredirox.com.key"))
