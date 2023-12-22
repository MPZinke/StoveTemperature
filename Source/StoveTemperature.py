#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2023.12.21                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import adafruit_mlx90640
from adafruit_minimqtt.adafruit_minimqtt import MQTT
import board
import busio
import ipaddress
import os
import socketpool
from time import sleep
import wifi
import os


# Setup Camera
I2C = busio.I2C(board.GP3, board.GP2, frequency=800000)
THERMAL_CAMERA = adafruit_mlx90640.MLX90640(I2C)
THERMAL_CAMERA.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

# Setup WiFi
WIFI_SSID = os.getenv("WIFI_SSID")
WIFI_PASSWORD = os.getenv("WIFI_PASSWORD")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
SOCKET_POOL = socketpool.SocketPool(wifi.radio)

# Setup MQTT
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

MQTT_CLIENT = MQTT(broker=MQTT_BROKER, username=MQTT_USER, password=MQTT_PASSWORD, socket_pool=SOCKET_POOL)
MQTT_CLIENT.connect()

AVG_TEMPERATURE_TOPIC = os.getenv("AVG_TEMPERATURE_TOPIC")
MAX_TEMPERATURE_TOPIC = os.getenv("MAX_TEMPERATURE_TOPIC")


class Optional:
	def __class_getitem__(cls, union_type) -> type:
		return union_type|type(None)


def get_picture_values() -> list[int]:
	frame = [0] * (32 * 24)

	try:
		THERMAL_CAMERA.getFrame(frame)
		return frame

	except ValueError:
		return None


def main():
	while(True):
		frame: list[int] = get_picture_values()

		average_temperature: int = sum(frame) // len(frame)
		highest_temperature: int = max(frame)

		MQTT_CLIENT.publish(AVG_TEMPERATURE_TOPIC, average_temperature)
		MQTT_CLIENT.publish(MAX_TEMPERATURE_TOPIC, highest_temperature)

		sleep(5)


main()
