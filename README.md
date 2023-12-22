# StoveTemperature
An MQTT microcontroller project to monitor stove and other thermal objects' temperatures using a thermal camera


## Purpose
The purpose of this device is to add better monitoring to potential fire hazards around the house, such as stoves and
candles. Stoves and candles, if left on and unattended can cause fires. This may not prevent people from forgetting to
turn off their stoves, but it can help remind them if they leave the house. While away, this project can provide
additional assurance that a stove was turned off.


## Details
This device is supposed to integrate into a Smart Home network over WiFi using the MQTT protocol. It works by taking a
thermal picture of an area and calculating the average temperature and maximum temperature of the picture's 768 pixels.
These values are then published to their respective MQTT feeds.

A Smart Home system can subscribe to these feeds and display or act based on the feeds' payloads. For example, if no one
is home and the payload reports a temperature over what is allowed, then the Smart Home system can notify that the stove
was left on. Additionally, if an owner is away, the payloads can be displayed to show the current temperature of the
stove and hopefully reassure the owner that the stove has been turned off.


## Requirements

### Hardware
- [ ] MLX90640 Thermal Camera breakout
- [ ] Raspberry Pi Pico W
	- [ ] Power cable & supply
- [ ] A safe container for these devices

### Other
- An MQTT broker


## Setup
Follow the instructions for your devices. In my case, I used Pimoroni's MLX90640 which has the below pins
```
 _______________________
 | GND     SCL SDA  3V |
 |  O   O   O   O   O  |
```
These connected to the Pico W as,

| MLX90640 | Pico W Pin Name(Number) |
|----------|-------------------------|
|    3V    | 3V Out (36)             |
|    SDA   | GP2 - I2C1 SDA (4)      |
|    SCL   | GP3 - I2C1 SCL (5)      |
|    GND   | GND (3)                 |

