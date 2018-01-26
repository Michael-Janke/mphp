#!/bin/bash
killall gunicorn
git --work-tree=/var/mp-server-deploy/ --git-dir=/var/mp-server-repo checkout -f
cd /var/mp-server-deploy/
pip3 install -r requirements.txt --user
python3 scripts/download_data.py
cd client
npm install
npm run build
cd ..
nohup /home/deploy/.local/bin/gunicorn -b 0.0.0.0:8080 -w 64 app:app --preload --timeout 360 > info.log 2> error.log &
