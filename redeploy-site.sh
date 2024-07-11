#!/bin/bash

cd /root/pe-portfolio-site

git fetch && git reset origin/main --hard

source env/bin/activate
pip install -r requirements.txt

systemctl daemon-reload
systemctl restart myportfolio
