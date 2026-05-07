import logging
import multiprocessing as mp
import socket
from typing import Optional

from dataclasses import dataclass

CTX = mp.get_context('spawn')
#: The log level to use
LOG_LEVEL = logging.DEBUG

#: The robomaster's video port
VIDEO_PORT: int = 40921
#: The robomaster's audio port
AUDIO_PORT: int = 40922
#: The port you send commands on
CTRL_PORT: int = 40923
#: The port that the robomaster pushes data on
PUSH_PORT: int = 40924
#: The port that the robomaster reports events on
EVENT_PORT: int = 40925
#: The IP Port TODO: figure out what this port is for
IP_PORT: int = 40926

#: The default buffer size TODO: figure out what this is used for so I can give a better description
DEFAULT_BUF_SIZE: int = 512

#: Constant to switch something on
SWITCH_ON: str = 'on'
#: Constant to switch something off
SWITCH_OFF: str = 'off'

#: Chassis lead movement mode
MODE_CHASSIS_LEAD: str = 'chassis_lead'
#: Gimbal lead movement mode
MODE_GIMBAL_LEAD: str = 'gimbal_lead'
#: Gimbal and chassis are independent movement mode
MODE_FREE: str = 'free'
#: A list of the mode enums
MODE_ENUMS = (MODE_CHASSIS_LEAD, MODE_GIMBAL_LEAD, MODE_FREE)

#: The armor hit constant
ARMOR_HIT: str = 'hit'
#: A list of the armor enums
ARMOR_ENUMS = (ARMOR_HIT,)

#: A string to indicate applause
SOUND_APPLAUSE: str = 'applause'
#: A list of the sound enums
SOUND_ENUMS = (SOUND_APPLAUSE,)

#: Indicates all of the LEDs
LED_ALL = 'all'
#: Indicates all of the gimbal LEDs
LED_TOP_ALL = 'top_all'
#: Indicates the right gimbal LED
LED_TOP_RIGHT = 'top_right'
#: Indicates the left gimbal LED
LED_TOP_LEFT = 'top_left'
#: Indicates all of the chassis LEDs
LED_BOTTOM_ALL = 'bottom_all'
#: Indicates the front chassis LED
LED_BOTTOM_FRONT = 'bottom_front'
#: Indicates the back chassis LED
LED_BOTTOM_BACK = 'bottom_back'
#: Indicates the left chassis LED
LED_BOTTOM_LEFT = 'bottom_left'
#: Indicates the right chassis LED
LED_BOTTOM_RIGHT = 'bottom_right'
#: A list of the LED enums
LED_ENUMS = (LED_ALL, LED_TOP_ALL, LED_TOP_RIGHT, LED_TOP_LEFT,
             LED_BOTTOM_ALL, LED_BOTTOM_FRONT, LED_BOTTOM_BACK,
             LED_BOTTOM_LEFT, LED_BOTTOM_RIGHT)

#: Indicates that an LED should stay solid
LED_EFFECT_SOLID = 'solid'
#: Indicates that an LED should be off
LED_EFFECT_OFF = 'off'
#: Indicates that an LED should pulse
LED_EFFECT_PULSE = 'pulse'
#: Indicates that an LED should blink
LED_EFFECT_BLINK = 'blink'
#: Indicates that an LED should scroll (only works for gimbal LEDs)
LED_EFFECT_SCROLLING = 'scrolling'
#: A list of the LED Effect enums
LED_EFFECT_ENUMS = (LED_EFFECT_SOLID, LED_EFFECT_OFF,
                    LED_EFFECT_PULSE, LED_EFFECT_BLINK,
                    LED_EFFECT_SCROLLING)