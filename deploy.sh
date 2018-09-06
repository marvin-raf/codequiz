#!/bin/bash

ssh rafg@rafaelgoesmann.com << EOF
cd websites/rafaelgoesmann.com && git fetch --all && git reset --hard origin/master && pm2 delete portfolio-website && NODE_ENV=production pm2 start server.js --name portfolio-website 
EOF
