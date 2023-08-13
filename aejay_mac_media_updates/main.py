import os
import ssl
import sys
import time
from typing import Literal, Optional
import keyring

import paho.mqtt.client as mqtt
from paho.mqtt import publish

def _get_credentials(cred_name: str) -> tuple[str, str]:
    username = keyring.get_password(cred_name, 'username')
    if username is None:
        raise Exception(f"cred {cred_name} username not found")
    password = keyring.get_password(cred_name, 'password')
    if password is None:
        raise Exception(f"cred {cred_name} password not found")
    return username, password

DeviceType = Literal["microphone", "camera"]
EventType = Literal["on", "off"]

def main(device: DeviceType, event: EventType):    

    mqtt_url = os.environ.get("AEJAY_MQTT_URL") or ""
    cred_name = os.environ.get("AEJAY_MQTT_CRED") or ""
    camera_topic = os.environ.get("AEJAY_MQTT_MAC_CAMERA_TOPIC") or ""
    microphone_topic = os.environ.get("AEJAY_MQTT_MAC_MICROPHONE_TOPIC") or ""

    # Assert that the environment variables are set
    if not mqtt_url:
        raise Exception("AEJAY_MQTT_URL must be set")
    if not cred_name:
        raise Exception("AEJAY_MQTT_CRED must be set")
    if not camera_topic:
        raise Exception("AEJAY_MQTT_MAC_CAMERA_TOPIC must be set")
    if not microphone_topic:
        raise Exception("AEJAY_MQTT_MAC_MICROPHONE_TOPIC must be set")

    topic = camera_topic if device == "camera" else microphone_topic
    body = event.upper()

    username, password = _get_credentials(cred_name)

    if event == "on":
        # Add a slight delay to account for race conditions when switching
        # between devices during a call.
        time.sleep(0.5)

    publish.single(
        topic=topic, 
        payload=body, 
        hostname=mqtt_url, 
        port=8884,
        auth={'username': username, 'password': password},
        tls={
            "ca_certs": None, # type: ignore
            "tls_version": ssl.PROTOCOL_TLSv1_2,
        },
        protocol=mqtt.MQTTv5,
        transport="websockets",
    )

if __name__ == "__main__":
    sys.stdout = sys.stderr = open("/tmp/aejay_mac_media_updates.log", "w")

    # Oversight will send in the following arguments:
    # -device <microphone|camera> -event <on|off> -pid <pid>
    # We only care about the device and event, parse them out
    # and pass them to the main function:
    device: Optional[DeviceType] = None
    event: Optional[EventType] = None
    for i, arg in enumerate(sys.argv):
        if arg == "-device":
            deviceArg = sys.argv[i + 1]
            if deviceArg not in ["microphone", "camera"]:
                raise Exception("device must be microphone or camera")
            device = deviceArg # type: ignore
        elif arg == "-event":
            eventArg = sys.argv[i + 1]
            if eventArg not in ["on", "off"]:
                raise Exception("event must be on or off")
            event = eventArg # type: ignore
    if not device or not event:
        raise Exception("device and event must be specified")
    # Assert that our device and event are valid
    main(device, event)
