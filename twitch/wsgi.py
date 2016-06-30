from twitch.web_app import create_app

if __name__ == '__main__':
    app = create_app.create_app()
    app.run(debug=False)
