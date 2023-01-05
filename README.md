# Overview
This project was intended for personal use. If you're interested in it, you probably want ddclient, which also supports google domains as of v3.9.0.

I wrote this because I have an irrational hatred of Perl, and all of my dynamic domains are through google. :)

# Running dnsupdater
- Copy example.env to .env
- Fill the parameters in `.env`. The username and password come from domains.google.com under "advanced settings".
- Run `docker-compose build`
- Run `docker-compose up -d`
