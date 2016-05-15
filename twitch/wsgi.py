from twitch.web_app import app

if __name__ == '__main__':
    inst = app.create_app()
    inst.run(debug=False)
