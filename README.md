# Cecilia sheet music manager

Let us first introduce this wonderful application. This is Cecilia. Named after the patron saint of musicians. With this web application it is possible to manage your orchestra's sheet music. It is possible to manage your orchestra's members and to define which part they play in your orchestra. It is also possible to upload your sheet music and to define it's key, what instrument the sheet music is for and for what part it is in your orchestra. In this way it is possible for the members of your orchestra to download all the necessary sheet music for a specific concert.

## How to set up
This application is a simple django application. If you want to set up this application on your server, all you have to do is create an environment configuration file in the root directory called `.env` and write down a set of environment variables

| Environment variable     | Purpose                                             |
|--------------------------|-----------------------------------------------------|
| DJANGO_DEBUG             | Control debug mode. Set to false in Production      |
| DJANGO_SECRET_KEY        | Encryption key. Should be random and kept secret    |
| DJANGO_ALLOWED_HOSTS     | Should be set to your proper domain name            |
| DJANGO_DATABASE_USER     | The username used to connect to the database        |
| DJANGO_DATABASE_PASSWORD | Database password to be used to connect to database |
| DJANGO_DB_NAME           | Name of schema to be used to connect to database    |
| DJANGO_DATABASE_HOST     | Hostname to of the database to be used              |
| DJANGO_EMAIL_HOST        | Hostname of th SMTP server used to send emails      |
| DJANGO_EMAIL_PORT        | Port of the SMTP server                             |

## Want to use Docker?

Another possibility is to use docker. This, however is only configured to be used in debug mode for the moment and should not be used in production. Everything to do this is contained in a docker compose file located in the root of the source tree plus a docker file to build an image of the web application. This docker compose file contains the following components.

| Component  | Explanation                                                                   |
|------------|-------------------------------------------------------------------------------|
| Cecilia    | The web application itself running on port 8000                               |
| MySQL      | A database server running on port 3306                                        |
| PhpMyAdmin | PhpMyadmin running on port 8080. Handy for managing the database              |
| Maildev    | An email client running on port 1080 plus an SMTP server running on port 1025 |
| Debugger   | A debug server runs on port 5678                                              |

All the emails sent by the application end up visible in the maildev email client

The proper way to run this is via a docker compose command executed in the root directory of the source tree

`docker compose up`