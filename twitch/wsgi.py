from twitch.create_wsgi import app as application

if __name__ == '__main__':
    application.run(debug=False)
