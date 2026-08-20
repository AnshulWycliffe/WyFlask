# Configuration

WyFlask uses class-based configuration. By default, it expects `WYFLASK_ENV` environment variable to define the environment (e.g., `development`, `production`).

You can override config simply passing a class or string to `create_app("app.config.MyConfig")`.
