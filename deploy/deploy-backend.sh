#!/bin/bash

ssh rafg@rafaelgoesmann.com << EOF
cd websites/codequiz.co.nz/ &&
git fetch --all &&
git reset --hard origin/master && 
cd frontend &&
npm install &&
npm run build &&
cd ../frontend-serve &&
pm2 stop codequiz-frontend &&
pm2 delete codequiz-frontend &&
NODE_ENV=production pm2 start index.js --name=codequiz-frontend &&
cd ../backend &&
pm2 stop codequiz-backend &&
pm2 delete codequiz-backend &&
pm2 start prod_server.sh --name=codequiz-backend

EOF
