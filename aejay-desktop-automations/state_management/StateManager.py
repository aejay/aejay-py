import pprint
from paho.mqtt import client as mqtt
from typing import Callable, Union
from datetime import datetime, timedelta
import ssl
from .RemoteState import RemoteState

class StateManager:
    def __init__(
        self,
        mqtt_server_url: str,
        mqtt_username: str,
        mqtt_password: str,
        mqtt_update_topic_name: str,
        mqtt_request_topic_name: str,
        on_update: Callable[[RemoteState], None] = lambda _: None
    ) -> None:
        self.mqtt_server_url = mqtt_server_url
        self.mqtt_update_topic_name = mqtt_update_topic_name
        self.mqtt_request_topic_name = mqtt_request_topic_name
        self._on_update = on_update
        self._has_published = False

        self.client = mqtt.Client(transport="websockets", protocol=mqtt.MQTTv5)
        self.client.ws_set_options(path="/")       
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
        self.client.username_pw_set(mqtt_username, mqtt_password)
        self.client.message_callback_add(mqtt_update_topic_name, self._on_message)
        self.client.reconnect_delay_set(min_delay=1, max_delay=120)
        # self.client.on_log = lambda client, userdata, level, buf: print(buf)
        self.client.on_connect = self._on_connect

    def _on_connect(
        self,
        client: mqtt.Client,
        userdata: object,
        flags: dict,
        rc: mqtt.ReasonCodes,
        properties: Union[mqtt.Properties, None]
    ) -> None:
        if rc == 0:
            session_present = flags.get("session present")
            client.subscribe(self.mqtt_update_topic_name)
            if session_present == 1:
                print("Connected to MQTT broker with existing session")
            else:
                print("Connected to MQTT broker with new session")
                if not self._has_published:
                    client.publish(self.mqtt_request_topic_name)
                    self._has_published = True
        else:
            print(f"Connection to MQTT failed with result {rc}")

    def _on_message(
        self,
        client: mqtt.Client,
        userdata: object,
        msg: mqtt.MQTTMessage
    ) -> None:
        state = RemoteState.from_json(msg.payload.decode("utf-8"))
        self._on_update(state)

    def Start(self):
        if not self.client.is_connected():
            self.client.connect(self.mqtt_server_url, 8884, 60)
            self.client.loop_start()

    def Stop(self):
        if self.client.is_connected():
            self.client.disconnect()
            self.client.loop_stop()
