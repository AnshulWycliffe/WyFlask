# Architecture

WyFlask is built on top of Flask and Werkzeug, leveraging their WSGI foundation while providing higher-level abstractions.

```
                    ┌─────────────────────┐
                    │    Application      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      WyFlask        │
                    │   Application Core  │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
     Module System        Configuration         Middleware
          │
          ▼
      Blueprint
          │
          ▼
       Routes
          │
          ▼
       Services
          │
          ▼
     Repositories
          │
          ▼
       Database
```
