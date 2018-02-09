from app import create_app

app = create_app('default')


if __name__ == '__main__':
    app.run(ssl_context=("ssl/www.fredirox.com.crt", "ssl/www.fredirox.com.key"))
