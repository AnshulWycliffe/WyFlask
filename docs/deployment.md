# Deployment

WyFlask exposes a normal Flask WSGI application.
You can deploy it using Gunicorn, Waitress, or uWSGI just as you would any Flask app.

```bash
gunicorn -w 4 'run:app'
```
