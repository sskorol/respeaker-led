## Respeaker LED Controller

This repository demonstrates how to control Respeaker Pixel Ring via MQTT.

### Installation

```shell script
git clone https://github.com/sskorol/respeaker-led.git && cd respeaker-led
./dependencies.sh
pip3 install -r requirements.txt
```

### Configuration

Adjust **config.json** with missing MQTT settings:
```json
{
  "mqttAddress": "127.0.0.1",
  "mqttUser": "",
  "mqttPassword": ""
}
```

### Running

```shell script
python3 runner.py
```

Now you can test different LED options by sending MQTT commands to the following topics:

- **respeaker/led/wake**: activates Pixel Ring with provided DOA. You have to provide a direction as int value in a payload.
- **respeaker/led/sleep**: deactivates Pixel Ring.
- **respeaker/led/think**: activates "thinking" pattern.
- **respeaker/led/speak**: activates "speaking" pattern.
- **respeaker/led/listen**: activates "listening" pattern.

Use any MQTT client for testing:
```shell script
mosquitto_pub -h ip -u username -P password -t respeaker/led/wake -m 140
```

### Respeaker Integration

You can use this project with [respeaker-websockets](https://github.com/sskorol/respeaker-websockets) which is already configured to control LEDs when hotword is detected and transcribe is received.
