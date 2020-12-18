# mqtt_apcups

Testing done on APC by Schneider Electric Back-UPS BX - BX1400UI, on raspbury pi 2b using USB.

Send's all stats using apcusbd over MQTT, there is also a Home assistant dicovery script 'h_a_config_topics.py'.

install apcusbd 'apt install apcusbd'
The manual can be found here
http://www.apcupsd.org/manual/manual.html#installation-from-source

You will need to fill in MQTT details, Run 'pub_stats.py' and subscribe to topic's.
I run the script every 5 minutes with cron job. cron example,
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
*/5 * * * *  python3 /path/to/script/pub_stats.py

If using with Home assistant run 'h_a_config_topics.py' once and this will set up topics.

Number values are converted to integers and the rest of the string is removed.

Example of some stats and mqtt output,

MODEL    : Back-UPS XS 1400U
apc_ups/sensor/UPS_MODEL/state Back-UPS XS 1400U

STATUS   : ONLINE
apc_ups/sensor/UPS_STATUS/state ONLINE

LINEV    : 240.0 Volts
apc_ups/sensor/UPS_LINEV/state 242

LOADPCT  : 9.0 Percent
apc_ups/sensor/UPS_LOADPCT/state 9

BCHARGE  : 100.0 Percent
apc_ups/sensor/UPS_BCHARGE/state 100

TIMELEFT : 64.2 Minutes
apc_ups/sensor/UPS_TIMELEFT/state 64

If you want message as string empty 'float_keys_list',

LINEV    : 240.0 Volts
apc_ups/sensor/UPS_LINEV/state 242.0 Volts
