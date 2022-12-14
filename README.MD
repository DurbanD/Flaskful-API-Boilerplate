# Flask REST Api Template

## Installation

Clone the repository, after which you can start the API by running `py app.py` in the root directory. API will then be available at localhost:5000 by default.

## Summary

This is a template for use in creating a Flask based RESTful API with user accounts. Uses SQLite as a database by default, and creates all nonexistant tables on startup. The two models, User and Session, are designed in a one-to-many relationship so that a single user account may have multiple authenticated sessions all with their own unique security tokens. 

## Endpoints

| Endpoint | Method | Description | Req. Headers | Result |
| --- | --- | --- | --- | --- |
| `/user/` | POST | Create a user | | Tokens |
| `/user/` | GET | Get a list of all users | Authorization (admin access) | User |
| `/user/<id>` | GET | Get a single user | Authorization (access) | User list |
| `/user/me` | GET | Get current user information | Authorization (access) | User | 
| `/user/<id>` | DELETE | Delete a User | Authorization (access) | User |
| `/auth/login` | POST | Login. Req "username" and "password" in payload |  | Tokens |
| `/auth/refresh` | GET | Request new tokens | Authorization (refresh); | Tokens |
| `/auth/check` | GET | Check access token status | Authorization (access); | `{authStatus: Bool, exp: Float }` |
| `/auth/logout` | POST | Logout | Authorization (access) | Status code |
| `/auth/<id>` | DELETE | Delete auth session | Authorization (access) | Status Code |
| `/auth/recover` | POST | Generate Temporary Token and Send Email | Username or Email | Temp Token |

All authorization tokens are passed to the server in the "Authorization" header. All requests require a Content-Type "application/json" header.

## Authentication and Security
Authentication is based on Auth0, using **bearer** access and refresh tokens while keeping a record of what User Agent the tokens were generated for. If a different user agent than the one used to create the session attempts to use that session's refresh key, the session will be deleted forcing that user agent to log in again to recieve new tokens. Access tokens are used to request any protected information, and quickly time out; Refresh tokens are used to generate new tokens.
Passwords are hashed with sha256 and never stored in plain text. 