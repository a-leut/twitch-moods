# twitch-moods
shows how twitch.tv chat is feeling

## chat_client

Connects to twitch.tv chat IRC chat, looks for emoticons, counts them, and stores the results in Redis.

## twitch_api_service

Gets info from twitch.tv including emoticons and chat channels.

## web_app

Flask app to serve the results from Redis.
