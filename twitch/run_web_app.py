from twitch.web_app import create_app

inst = create_app.create_app()
inst.run(debug=True)
