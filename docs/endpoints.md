# API Endpoints

Everywhere below we suppose authentication router mounted as `/auth` prefix.

## Endpoints

### GET, POST `/auth/login`

### POST /auth/logout

### GET /auth/profile

### POST /auth/change_password

### POST /auth/change_email

### GET /auth/settings.js

### GET /auth/signup

### POST /auth/users

### GET, POST /auth/emailverify/{email}

GET: HTML page to verify email

POST: checks if user-submitted code found in database and performs action (either set email_verified or changes email)

### POST /auth/emailverify_resend/{email}
If can resend code (settings.code_regenerate passed since code was sent), deletes old code and sends new one.

### GET, POST /auth/recover
GET: HTML page
POST: send recovery request to email specified in form

### GET, POST /auth/recover/{email}
GET: HTML page
POST: sent new password for user (if code matches)


### POST /auth/jwt/get

### POST /auth/jwt/refresh

### GET /auth/static/...
static files
