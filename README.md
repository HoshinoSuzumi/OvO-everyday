# OvO-everyday

Server side implementation in python for [OvO](https://github.com/ovojs/OvO)

OvO is a great self-deployed comment system

[![wakatime](https://wakatime.com/badge/github/HoshinoSuzumi/OvO-everyday.svg)](https://wakatime.com/badge/github/HoshinoSuzumi/OvO-everyday)

~~Pigeon Oriented Programming~~

# Features

## Email notification

**Basic functions**

- [x] Reply notification
- [x] Mention parse and notification

**Protocol support**

- [x] Exchange support
- [x] SMTP support

**Extra functions**

- [x] Custom HTML template

## Security

**XSS Filter**

- [x] Whitelist of HTML tags and attributes
- [x] Blacklist of value of attributes

## Data storage

> SQLite is easy to migrate, deploy and manage. So currently it will not support other databases

- [x] SQLite

# Deployment

```bash
pip install fastapi uvicorn[standard]
uvicorn main:app
```

# Document

Once you have completed the deployment, you can access API documents via visiting `http://[ip-address]/docs`
