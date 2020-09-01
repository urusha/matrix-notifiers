# Zabbix Matrix notifiers
Simple Zabbix Matrix notifiers (message and call). Use plain (no-e2e) events. Require python 3 with requests, urllib3, markdown, beautifulsoup4 modules.
`zabbix-matrix-call.py` doesn't honor message text (third arg) and skips alerts with the subject starting with `OK`.

## Install
apt:
```
apt-get install python3 python3-requests python3-urllib3 python3-markdown python3-bs4
```
pip:
```
pip3 install requests urllib3 Markdown beautifulsoup4
```
Put scripts in `/usr/lib/zabbix/alertscripts`

Modify `URL` and `TOKEN` variables using your matrix-synapse server url and user's access_token string.

Create new Media type in zabbix (Administration - Media types - Create media type) with `Type` = `Script`, `Script name` = `zabbix-matrix.py` or `zabbix-matrix-call.py`, `Script parameters`: `{ALERT.SENDTO}` , `{ALERT.SUBJECT}`, `{ALERT.MESSAGE}`.

## Usage
Add new Media to the desired zabbix user and set `Send to` to internal room ID of the desired matrix room (e.g. `!xfsdaflgughalf:example.com`, to get this ID - go to the room's `Settings` -> `Advanced` in Riot/Element). Matrix user used by the scripts (with access_token `TOKEN`) should be invited and joined to this room.

To be able to send messages to a group chat, additional user should be created in zabbix (granted read access to the required zabbix hosts), with Media `Send to` set to the desired group chat room id.
