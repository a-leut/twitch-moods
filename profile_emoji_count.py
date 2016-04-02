from web_app.app import create_app
from web_app.views import get_emoji_counts

app = create_app()
with app.app_context():
    print(get_emoji_counts())
