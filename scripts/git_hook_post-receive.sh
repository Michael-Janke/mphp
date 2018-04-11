#!/bin/bash
killall python3
git --work-tree=/var/mp-server-deploy/ --git-dir=/var/mp-server-repo checkout -f
cd /var/mp-server-deploy/
pip3 install -r requirements.txt --user
python3 scripts/download_data.py
cd client
npm install
npm run build
cd ..
nohup python3 app.py -t -P 8080 -H 0.0.0.0 > info.log 2> error.log &
sleep 10 && cat error.log