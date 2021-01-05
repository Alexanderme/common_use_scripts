#/bin/bash
source /etc/profile
cp /usr/local/ev_sdk/3rd/license/v20_0/bin/ev_license /usr/local/ev_sdk/authorization
cp /usr/local/ev_sdk/3rd/license/bin/ev_license /usr/local/ev_sdk/authorization
cd /usr/local/ev_sdk/authorization
chmod +x ev_license
./ev_license -r r.txt
./ev_license -l privateKey.pem r.txt license.txt





