#!/bin/sh

set -e

mkdir -p /opt/grafana2matrix/
cp grafana2matrix.py /opt/grafana2matrix/
cp grafana2matrix.service /etc/systemd/system/
chown root:grafana /opt/grafana2matrix/grafana2matrix.py
chmod 0750 /opt/grafana2matrix/grafana2matrix.py

echo "grafana2matrix installation successful!"
