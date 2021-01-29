#!/bin/sh

set -e

cp zabbix-matrix*.py /usr/lib/zabbix/alertscripts/
chown root:zabbix /usr/lib/zabbix/alertscripts/zabbix-matrix*.py
chmod 0750 /usr/lib/zabbix/alertscripts/zabbix-matrix*.py

echo "zabbix-matrix installation successful!"
