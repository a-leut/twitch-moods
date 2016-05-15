from twitch.web_app import app

inst = app.create_app()
inst.run(debug=True)
