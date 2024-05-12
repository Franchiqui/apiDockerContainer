echo 'Running server...'
gunicorn --env, main:app, --reload, --host, 0.0.0.0:$PORT