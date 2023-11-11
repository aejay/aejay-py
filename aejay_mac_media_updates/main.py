"""Main module for a module that handles sending media updates to HASS"""
import os
import ssl
import sys
from datetime import datetime
from typing import Literal, Optional

import paho.mqtt.client as mqtt
from paho.mqtt import publish

from aejay_common.credential_management import get_credentials


DeviceType = Literal["microphone", "camera"]
EventType = Literal["on", "off"]


def _handle_device_event(device: DeviceType, event: EventType):
    mqtt_url = os.environ.get("AEJAY_MQTT_URL") or ""
    cred_name = os.environ.get("AEJAY_MQTT_CRED") or ""
    camera_topic = os.environ.get("AEJAY_MQTT_MAC_CAMERA_TOPIC") or ""
    microphone_topic = os.environ.get("AEJAY_MQTT_MAC_MICROPHONE_TOPIC") or ""

    # Assert that the environment variables are set
    if not mqtt_url:
        raise ValueError("AEJAY_MQTT_URL must be set")
    if not cred_name:
        raise ValueError("AEJAY_MQTT_CRED must be set")
    if not camera_topic:
        raise ValueError("AEJAY_MQTT_MAC_CAMERA_TOPIC must be set")
    if not microphone_topic:
        raise ValueError("AEJAY_MQTT_MAC_MICROPHONE_TOPIC must be set")

    topic = camera_topic if device == "camera" else microphone_topic
    body = event.upper()

    username, password = get_credentials(cred_name)

    # if event == "on":
    #     # Add a slight delay to account for race conditions when switching
    #     # between devices during a call.
    #     time.sleep(0.5)

    # Print what we're updating, for the log
    print(f"{datetime.now().astimezone().isoformat()} Updating {device} to {event}")

    publish.single(
        topic=topic,
        payload=body,
        hostname=mqtt_url,
        port=8884,
        auth={"username": username, "password": password},
        tls={
            "ca_certs": None,  # type: ignore
            "tls_version": ssl.PROTOCOL_TLSv1_2,
        },
        protocol=mqtt.MQTTv5,
        transport="websockets",
    )

    print(f"{datetime.now().astimezone().isoformat()} Updated {device} to {event}")


def main():
    """
    The main entry point for the module from command line.
    """
    with open("/tmp/aejay_mac_media_updates.log", "a", encoding="utf-8") as f:
        sys.stdout = sys.stderr = f
        # Oversight will send in the following arguments:
        # -device <microphone|camera> -event <on|off> -process <pid> -activeCount <0..n>
        # We only care about the device and event, parse them out
        # and pass them to the main function:
        device: Optional[DeviceType] = None
        event: Optional[EventType] = None
        activeCount: Optional[int] = None
        for i, arg in enumerate(sys.argv):
            if arg == "-device":
                device_arg = sys.argv[i + 1]
                if device_arg not in ["microphone", "camera"]:
                    raise ValueError("device must be microphone or camera")
                device = device_arg  # type: ignore
            elif arg == "-event":
                event_arg = sys.argv[i + 1]
                if event_arg not in ["on", "off"]:
                    raise ValueError("event must be on or off")
                event = event_arg  # type: ignore
            elif arg == "-activeCount":
                val = sys.argv[i + 1]
                if not val.isdigit():
                    raise ValueError("activeCount must be an integer")
                activeCount = int(val)
        if not device or not event:
            raise ValueError("device and event must be specified")
        if activeCount is not None:
            if event == "on" and activeCount > 0:
                _handle_device_event(device, "on")
            elif event == "off" and activeCount <= 0:
                _handle_device_event(device, "off")
        else:
            _handle_device_event(device, event)

    # Set stdout and stderr back to normal
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

if __name__ == "__main__":
    main()
