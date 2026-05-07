# -*- coding: utf-8 -*-

# ██████╗  ██████╗ ██████╗  ██████╗ ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ ██████╗ ██╗   ██╗
# ██╔══██╗██╔═══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝
# ██████╔╝██║   ██║██████╔╝██║   ██║██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝██████╔╝ ╚████╔╝
# ██╔══██╗██║   ██║██╔══██╗██║   ██║██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗██╔═══╝   ╚██╔╝
# ██║  ██║╚██████╔╝██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║██║        ██║
# ╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝        ╚═╝

import logging
import multiprocessing as mp
import socket
from typing import Optional

from dataclasses import dataclass

CTX = mp.get_context('spawn')
LOG_LEVEL = logging.DEBUG

VIDEO_PORT: int = 40921
AUDIO_PORT: int = 40922
CTRL_PORT: int = 40923
PUSH_PORT: int = 40924
EVENT_PORT: int = 40925
IP_PORT: int = 40926

DEFAULT_BUF_SIZE: int = 512

# switch_enum
SWITCH_ON: str = 'on'
SWITCH_OFF: str = 'off'

# mode_enum
MODE_CHASSIS_LEAD: str = 'chassis_lead'
MODE_GIMBAL_LEAD: str = 'gimbal_lead'
MODE_FREE: str = 'free'
MODE_ENUMS = (MODE_CHASSIS_LEAD, MODE_GIMBAL_LEAD, MODE_FREE)

# armor_event_attr_enum
ARMOR_HIT: str = 'hit'
ARMOR_ENUMS = (ARMOR_HIT,)

# sound_event_attr_enum
SOUND_APPLAUSE: str = 'applause'
SOUND_ENUMS = (SOUND_APPLAUSE,)

# led_comp_enum
LED_ALL = 'all'
LED_TOP_ALL = 'top_all'
LED_TOP_RIGHT = 'top_right'
LED_TOP_LEFT = 'top_left'
LED_BOTTOM_ALL = 'bottom_all'
LED_BOTTOM_FRONT = 'bottom_front'
LED_BOTTOM_BACK = 'bottom_back'
LED_BOTTOM_LEFT = 'bottom_left'
LED_BOTTOM_RIGHT = 'bottom_right'
LED_ENUMS = (LED_ALL, LED_TOP_ALL, LED_TOP_RIGHT, LED_TOP_LEFT,
             LED_BOTTOM_ALL, LED_BOTTOM_FRONT, LED_BOTTOM_BACK,
             LED_BOTTOM_LEFT, LED_BOTTOM_RIGHT)

# led_effect_enum
LED_EFFECT_SOLID = 'solid'
LED_EFFECT_OFF = 'off'
LED_EFFECT_PULSE = 'pulse'
LED_EFFECT_BLINK = 'blink'
LED_EFFECT_SCROLLING = 'scrolling'
LED_EFFECT_ENUMS = (LED_EFFECT_SOLID, LED_EFFECT_OFF,
                    LED_EFFECT_PULSE, LED_EFFECT_BLINK,
                    LED_EFFECT_SCROLLING)


@dataclass
class ChassisSpeed:
    """
    A class describing the chassis's speed

    Attributes
    ----------

    x: float
        The speed of the chassis in the x-direction (forward/backward) in m/s
    y: float
        The speed of the chassis in the y-direction (left-right) in m/s
    z: float
        The angular speed of the chassis's rotation (clockwise, counterclockwise) in degrees/s
    w1: int
        The speed of the front-right mecanum wheel in rpm
    w2: int
        The speed of the front-left mecanum wheel in rpm
    w3: int
        The speed of the back-right mecanum wheel in rpm
    w4: int
        The speed of the back-left mecanum wheel in rpm
    """
    x: float
    y: float
    z: float
    w1: int
    w2: int
    w3: int
    w4: int


@dataclass
class ChassisPosition:
    """
    A class describing the chassis's position (Usually its relative position for the purposes of moving the chassis)

    Attributes
    ----------

    x: float
        The forward-backward position of the chassis in m
    y: float
        The left-right position of the chassis in m
    z: float
        The clockwise-counterclockwise rotation of the chassis in degrees
    """
    x: float
    y: float
    z: Optional[float]


@dataclass
class ChassisAttitude:
    """
    A class describing the chassis's rotation in 3D space

    Attributes
    ----------
    pitch: float
        The pitch of the chassis in degrees
    roll: float
        The roll of the chassis in degrees
    yaw: float
        The yaw of the chassis in degrees
    """
    pitch: float
    roll: float
    yaw: float


@dataclass
class ChassisStatus:
    """
    A class describing several current statuses of the chassis

    Attributes
    ----------
    static: bool
        True if the chassis is not moving
    uphill: bool
        True if the chassis is going uphill
        TODO: Determine if this means going *forward* uphill
    downhill: bool
        True if the chassis is going downhill
        TODO: Determine if this means going *forward* downhill
    on_slope: bool
        True if the chassis is on a slope
    pick_up: bool
        True if the chassis is being held by a person
    slip: bool
        True if the chassis is slipping
    impact_x: bool
        True if the chassis senses an impact on the x-axis
    impact_y: bool
        True if the chassis senses an impact on the y-axis
    impact_z: bool
        True if the chassis senses an impact on the z-axis
        TODO: Determine if this means up/down, or clockwise/counterclockwise
    roll_over: bool
        True if the chassis is rolled over
    hill_static:
        True if the chassis is not moving on a slope
    """
    static: bool
    uphill: bool
    downhill: bool
    on_slope: bool
    pick_up: bool
    slip: bool
    impact_x: bool
    impact_y: bool
    impact_z: bool
    roll_over: bool
    hill_static: bool


@dataclass
class GimbalAttitude:
    """
    A class describing the gimbal's rotation in 3D space

    Attributes
    ----------

    pitch: float
        The pitch of the gimbal in degrees
    yaw: float
        The yaw of the gimbal in degrees
    """
    pitch: float
    yaw: float


@dataclass
class ArmorHitEvent:
    """
    A class describing an armor hit event

    Attributes
    ----------

    index: int
        The index of the armor plate that was hit

        1: the rear of the chassis  
        2: the front of the chassis  
        3: the left of the chassis  
        4: the right of the chassis  
        5: the left of the gimbal  
        6: the right of the gimbal  
    type: int
        The type of hit detected by the armor plate

        0: A water bead hit  
        1: A strike TODO: determine what a "strike" is  
        2: A hand hit
    """
    index: int
    type: int


@dataclass
class SoundApplauseEvent:
    """
    A class describing a sound applause event

    Attributes
    ----------
    count: int
        The number of hand claps detected
    """
    count: int


def get_broadcast_ip(timeout: float = None) -> str:
    """
    Determine the broadcasting IP of Robomaster. Useful when the robomaster is in router mode

    :param timeout: how long to wait before timeout in seconds
    :return: IP of Robomaster.
    """

    #TODO: I'm not sure if this function actually determines the broadcasting IP of the robomaster when it's in router mode
    BROADCAST_INITIAL: str = 'robot ip '

    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.bind(('', IP_PORT))
    conn.settimeout(timeout)
    msg, ip, port = None, None, None
    try:
        msg, (ip, port) = conn.recvfrom(DEFAULT_BUF_SIZE)
    finally:
        conn.close()
    msg = msg.decode()
    assert len(msg) > len(BROADCAST_INITIAL), f'broken msg from {ip}:{port}: {msg}'
    msg = msg[len(BROADCAST_INITIAL):]
    assert msg == ip, f'unmatched source({ip}) and reported IP({msg})'
    return msg


class Commander:
    def __init__(self, ip: str = '', timeout: float = 30):
        """
        Create a new commander instance and connect it to Robomaster. This is what you use to control the robomaster when using this library

        :param ip:(Optional) IP of Robomaster, which can be detected automatically under router mode
        :param timeout:(Optional) TCP timeout in seconds
        """
        self._mu: mp.Lock = CTX.Lock()
        with self._mu:
            if ip == '':
                ip = get_broadcast_ip(timeout)
            self._ip: str = ip
            self._closed: bool = False
            self._conn: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._timeout: float = timeout
            self._conn.settimeout(self._timeout)
            self._conn.connect((self._ip, CTRL_PORT))
            resp = self._do('command')
            assert self._is_ok(resp) or resp == 'Already in SDK mode', f'entering SDK mode: {resp}'

    def close(self):
        """
        Close the commander instance, deallocate system socket resources.
        This method will NOT send quit command to Robomaster,
        because there may be other commanders still active.
        """
        with self._mu:
            self._conn.close()
            self._closed = True

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    @staticmethod
    def _is_ok(resp: str) -> bool:
        return resp == 'ok'

    def _do(self, *args) -> str:
        assert len(args) > 0, 'empty arg not accepted'
        assert not self._closed, 'connection is already closed'
        cmd = ' '.join(map(str, args)) + ';'
        self._conn.send(cmd.encode())
        buf = self._conn.recv(DEFAULT_BUF_SIZE)
        # 返回值后面有时候会多一个迷之空格，
        # 为了可能的向后兼容，额外剔除终止符。
        return buf.decode().strip(' ;')

    def get_ip(self) -> str:
        """
        Get the IP that the commander is currently connected to

        :return: IP that the commander is currently connected to
        """
        assert not self._closed, 'connection is already closed'
        return self._ip

    def do(self, *args) -> str:
        """
        Send a raw command to the robomaster

        :param args: The content of the raw command
        :return: The robomaster's response to the raw command
        """
        with self._mu:
            return self._do(*args)

    def version(self) -> str:
        """
        Query the robomaster's SDK version

        :return: The SDK version string - in format XX.XX.XX.XX
        """
        return self.do('version')

    def robot_mode(self, mode: str) -> str:
        """
        Change the Robomaster's movement mode.

        :param mode: The new movement mode, refer to enum MODE_*
        :return: ok, or raise certain exception.
        :raise unknown mode {mode}: The mode you gave was unknown 
        """
        #TODO: Figure out how to have a colon in the raise segment of this docstring
        assert mode in MODE_ENUMS, f'unknown mode: {mode}'
        resp = self.do('robot', 'mode', mode)
        assert self._is_ok(resp), f'robot_mode: {resp}'
        return resp

    def get_robot_mode(self) -> str:
        """
        Get the robomaster's current movement mode

        :return: The robomaster's movement mode, refer to enum MODE_*
        :raise unexpected robot mode: The received mode was unknown
        """
        resp = self.do('robot', 'mode', '?')
        assert resp in MODE_ENUMS, f'unexpected robot mode result: {resp}'
        return resp

    def chassis_speed(self, x: float = 0, y: float = 0, z: float = 0) -> str:
        """
        Update the chassis speed parameters

        :param x: speed in the forward-backward direction, in m/s
        :param y: speed in the left-right direction, in m/s
        :param z: rotation speed of the chassis, in degrees/s
        :return: ok, or raise certain exception.
        :raise x is out of range: The x value passed was outside of the range of -3.5 to 3.5 m/s
        :raise y is out of range: The y value passed was outside of the range of -3.5 to 3.5 m/s
        :raise z is out of range: The z value passed was outside of the range of -600 to 600 degrees/s
        """
        assert -3.5 <= x <= 3.5, f'x {x} is out of range'
        assert -3.5 <= y <= 3.5, f'y {y} is out of range'
        assert -600 <= z <= 600, f'z {z} is out of range'
        resp = self.do('chassis', 'speed', 'x', x, 'y', y, 'z', z)
        assert self._is_ok(resp), f'chassis_speed: {resp}'
        return resp

    def get_chassis_speed(self) -> ChassisSpeed:
        """
        Get the robomaster's chassis speed

        :return ChassisSpeed:
            An object of type ChassisSpeed (See ChassisSpeed class documentation) 
        """
        resp = self.do('chassis', 'speed', '?')
        ans = resp.split(' ')
        assert len(ans) == 7, f'get_chassis_speed: {resp}'
        return ChassisSpeed(x=float(ans[0]), y=float(ans[1]), z=float(ans[2]), w1=int(ans[3]), w2=int(ans[4]), w3=int(ans[5]), w4=int(ans[6]))

    def chassis_wheel(self, w1: int = 0, w2: int = 0, w3: int = 0, w4: int = 0) -> str:
        """
        Change the rotation speed of each individual wheel of the chassis

        :param w1: right front wheel speed(rpm)
        :param w2: left front wheel speed(rpm)
        :param w3: right back wheel speed(rpm)
        :param w4: left back wheel speed(rpm)
        :return ok: ok, or raise certain exception.
        :raise w{i} is out of range: The wheel speed you gave for wheel of index i was outside the range of -1000 to 1000
        """
        for i, v in enumerate((w1, w2, w3, w4)):
            assert -1000 <= v <= 1000, f'w{i + 1} {v} is out of range'
        resp = self.do('chassis', 'wheel', 'w1', w1, 'w2', w2, 'w3', w3, 'w4', w4)
        assert self._is_ok(resp), f'chassis_wheel: {resp}'
        return resp

    def chassis_move(self, x: float = 0, y: float = 0, z: float = 0, speed_xy: float = None, speed_z: float = None) -> str:
        """
        Make the chassis move relative to where it is now

        :param x: movement forward or backward, in meters (range: -5 to 5)
        :param y: movement left or right, in meters (range: -5 to 5)
        :param z: rotation clockwise or counterclockwise, in degrees (range: -1800 to 1800)
        :param speed_xy: translational speed (forward, backward, left, right) in meters/second (range: 0 to 3.5)
        :param speed_z: rotational speed in degrees/second (range: 0 to 600)
        :return ok: ok, or raise certain exception.
        :raise x is out of range: your x position is outside the range of -5 to 5 meters
        :raise y is out of range: your y position is outside the range of -5 to 5 meters
        :raise z is out of range: your z rotation is outside the range of -1800 to 1800 degrees
        """
        assert -5 <= x <= 5, f'x {x} is out of range'
        assert -5 <= y <= 5, f'y {y} is out of range'
        assert -1800 <= z <= 1800, f'z {z} is out of range'
        assert speed_xy is None or 0 < speed_xy <= 3.5, f'speed_xy {speed_xy} is out of range'
        assert speed_z is None or 0 < speed_z <= 600, f'speed_z {speed_z} is out of range'
        cmd = ['chassis', 'move', 'x', x, 'y', y, 'z', z]
        if speed_xy is not None:
            cmd += ['vxy', speed_xy]
        if speed_z is not None:
            cmd += ['vz', speed_z]
        resp = self.do(*cmd)
        assert self._is_ok(resp), f'chassis_move: {resp}'
        return resp

    def get_chassis_position(self) -> ChassisPosition:
        """
        Get the chassis position relative to where the robomaster powered on

        :return ChassisPosition: An object of type ChassisPosition (See ChassisPosition Documentation)
        """
        resp = self.do('chassis', 'position', '?')
        ans = resp.split(' ')
        assert len(ans) == 3, f'get_chassis_position: {resp}'
        return ChassisPosition(float(ans[0]), float(ans[1]), float(ans[2]))

    def get_chassis_attitude(self) -> ChassisAttitude:
        """
        Get the current attitude of the chassis (pitch, roll, yaw)

        :return ChassisAttitude: An object of type ChassisAttitude (See ChassisAttitude Documentation)
        TODO: Determine if the yaw is relative to the robot's starting position
        """
        resp = self.do('chassis', 'attitude', '?')
        ans = resp.split(' ')
        assert len(ans) == 3, f'get_chassis_attitude: {resp}'
        return ChassisAttitude(float(ans[0]), float(ans[1]), float(ans[2]))

    def get_chassis_status(self) -> ChassisStatus:
        """
        Get a list of statuses about the chassis
        
        :return: An object of type ChassisStatus (See ChassisStatus Documentation)
        """
        resp = self.do('chassis', 'status', '?')
        ans = resp.split(' ')
        assert len(ans) == 11, f'get_chassis_status: {resp}'
        return ChassisStatus(*map(lambda x: bool(int(x)), ans))

    def chassis_push_on(self, position_freq: int = None, attitude_freq: int = None, status_freq: int = None, all_freq: int = None) -> str:
        """
        Enable a repetitive transmission of chassis information at a specified frequency for specified attributes
        
        :param position_freq: The frequency at which the robomaster will transmit its chassis position in 1, 5, 10, 20, 30, or 50 Hz 
        :param attitude_freq: The frequency at which the robomaster will transmit its chassis attitude in 1, 5, 10, 20, 30, or 50 Hz
        :param status_freq: The frequency at which the robomaster will transmit its chassis statue in 1, 5, 10, 20, 30, or 50 Hz
        :param all_freq: The frequency at which all attributes will be transmitted in 1, 5, 10, 20, 30, or 50 Hz
        :return: ok, or raise certain exception.
        :raise all_freq is not valid: The all_freq value you gave was not 1, 5, 10, 20, 30, or 50 Hz
        :raise position_freq is not valid: The position_freq value you gave was not 1, 5, 10, 20, 30, or 50 Hz
        :raise attitude_freq is not valid: The attitude_freq value you gave was not 1, 5, 10, 20, 30, or 50 Hz
        :raise status_freq is not valid: The status_freq value you gave was not 1, 5, 10, 20, 30, or 50 Hz
        :raise at least one argument should not be None: You didn't give a frequency for any of the arguments, and therefore you called this function for it to do nothing
        """
        valid_frequencies = (1, 5, 10, 20, 30, 50)
        cmd = ['chassis', 'push']
        if all_freq is not None:
            assert all_freq in valid_frequencies, f'all_freq {all_freq} is not valid'
            cmd += ['freq', all_freq]
        else:
            if position_freq is not None:
                assert position_freq in valid_frequencies, f'position_freq {position_freq} is not valid'
                cmd += ['position', SWITCH_ON, 'pfreq', position_freq]
            if attitude_freq is not None:
                assert attitude_freq in valid_frequencies, f'attitude_freq {attitude_freq} is not valid'
                cmd += ['attitude', SWITCH_ON, 'afreq', attitude_freq]
            if status_freq is not None:
                assert status_freq in valid_frequencies, f'status_freq {status_freq} is not valid'
                cmd += ['status', SWITCH_ON, 'sfreq', status_freq]
        assert len(cmd) > 2, 'at least one argument should not be None'
        resp = self.do(*cmd)
        assert self._is_ok(resp), f'chassis_push_on: {resp}'
        return resp

    def chassis_push_off(self, position: bool = False, attitude: bool = False, status: bool = False, all: bool = False) -> str:
        """
        Disable the repetitive transmission of chassis information for specified attributes

        :param position: If True, disables the transmission of chassis position information
        :param attitude: If True, disables the transmission of chassis attitude information
        :param status: If True, disables the transmission of chassis status information
        :param all: If True, disables the transmission of all chassis information
        :return: ok, or raise certain exception.
        :raise at least one argument should be True: You passed all False statements, and calling this function had no point
        """
        cmd = ['chassis', 'push']
        if all or position:
            cmd += ['position', SWITCH_OFF]
        if all or attitude:
            cmd += ['attitude', SWITCH_OFF]
        if all or status:
            cmd += ['status', SWITCH_OFF]

        assert len(cmd) > 2, 'at least one argument should be True'
        resp = self.do(*cmd)
        assert self._is_ok(resp), f'chassis_push_off: {resp}'
        return resp

    def gimbal_speed(self, pitch: float, yaw: float) -> str:
        """
        Update the gimbal's rotation speed

        :param pitch: The gimbal's pitch speed in degrees/second (range: -450 to 450)
        :param yaw: The gimbal's yaw speed in degrees/second (range: -450 to 450)
        :return: ok, or raise certain exception.
        :raise pitch is out of range: The pitch speed you gave was out of the range of -450 to 450 degrees/second
        :raise yaw is out of range: The yaw speed you gave was out of the range of -450 to 450 degrees/second
        """
        assert -450 <= pitch <= 450, f'pitch {pitch} is out of range'
        assert -450 <= yaw <= 450, f'yaw {yaw} is out of range'
        resp = self.do('gimbal', 'speed', 'p', pitch, 'y', yaw)
        assert self._is_ok(resp), f'gimbal_speed: {resp}'
        return resp

    def gimbal_move(self, pitch: float = 0, yaw: float = 0, pitch_speed: float = None, yaw_speed: float = None) -> str:
        """
        Make the gimbal rotate to a new orientation, relative to its current orientation

        :param pitch: The change of the pitch in degrees (range: -55 to 55)
        :param yaw: The change of the yaw in degrees (range: -55 to 55)
        :param pitch_speed: The speed of the pitch change in degrees per second (range: 0 to 540)
        :param yaw_speed: The speed of the yaw change in degrees per second (range: 0 to 540)
        :return: ok, or raise certain exception.
        :raise pitch is out of range: The pitch you gave is outside the range of -55 to 55 degrees
        :raise yaw is out of range: The yaw you gave is outside the range of -55 to 55 degrees
        :raise pitch_speed is out of range: The pitch speed you gave is outside the range of 0 to 540 degrees/second
        :raise yaw_speed is out of range: The yaw speed you gave is outside the range of 0 to 540 degrees/second
        """
        assert -55 <= pitch <= 55, f'pitch {pitch} is out of range'
        assert -55 <= yaw <= 55, f'yaw {yaw} is out of range'
        assert pitch_speed is None or 0 < pitch_speed <= 540, f'pitch_speed {pitch_speed} is out of range'
        assert yaw_speed is None or 0 < yaw_speed <= 540, f'yaw_speed {yaw_speed} is out of range'
        cmd = ['gimbal', 'move', 'p', pitch, 'y', yaw]
        if pitch_speed is not None:
            cmd += ['vp', pitch_speed]
        if yaw_speed is not None:
            cmd += ['vy', yaw_speed]
        resp = self.do(*cmd)
        assert self._is_ok(resp), f'gimbal_move: {resp}'
        return resp

    def gimbal_moveto(self, pitch: float = 0, yaw: float = 0, pitch_speed: float = None, yaw_speed: float = None) -> str:
        """
        Make the gimbal rotate to an absolute orientation, relative to looking straight ahead, forward

        :param pitch: the absolute pitch in degrees (range: -25 to 30)
        :param yaw: the absolute yaw in degrees (range: -250 to 250)
        :param pitch_speed: the speed of the pitch change in degrees/second (range: 0 to 540)
        :param yaw_speed: the speed of the yaw change in degrees/second (range: 0 to 540)
        :return: ok, or raise certain exception.
        :raise pitch is out of range: The pitch you gave is out of the range of -25 to 30 degrees
        :raise yaw is out of range: The yaw you gave is out of the range of -250 to 250 degrees
        :raise pitch_speed is out of range: The pitch speed you gave is out of the range of 0 to 540 degrees/second
        :raise yaw_speed is out of range: The yaw speed you gave is out of the range of 0 to 540 degrees/second
        """
        assert -25 <= pitch <= 30, f'pitch {pitch} is out of range'
        assert -250 <= yaw <= 250, f'yaw {yaw} is out of range'
        assert pitch_speed is None or 0 < pitch_speed <= 540, f'pitch_speed {pitch_speed} is out of range'
        assert yaw_speed is None or 0 < yaw_speed <= 540, f'yaw_speed {yaw_speed} is out of range'
        cmd = ['gimbal', 'moveto', 'p', pitch, 'y', yaw]
        if pitch_speed is not None:
            cmd += ['vp', pitch_speed]
        if yaw_speed is not None:
            cmd += ['vy', yaw_speed]
        resp = self.do(*cmd)
        assert self._is_ok(resp), f'gimbal_moveto: {resp}'
        return resp

    def gimbal_suspend(self):
        """
        Put the gimbal to sleep by turning off all of its motors
        TODO: Determine if this turns off the gimbal lights too

        :return: ok
        """
        resp = self.do('gimbal', 'suspend')
        assert self._is_ok(resp), f'gimbal_suspend: {resp}'
        return resp

    def gimbal_resume(self):
        """
        Wake the gimbal back up by turning on all of its motors

        :return: ok
        """
        resp = self.do('gimbal', 'resume')
        assert self._is_ok(resp), f'gimbal_resume: {resp}'
        return resp

    def gimbal_recenter(self):
        """
        Recenter the gimbal.

        :return: ok
        """
        resp = self.do('gimbal', 'recenter')
        assert self._is_ok(resp), f'gimbal_recenter: {resp}'
        return resp

    def get_gimbal_attitude(self) -> GimbalAttitude:
        """
        Get the gimbal's attitude in pitch and yaw

        :return GimbalAttitude: An object of GimbalAttitude (see GimbalAttitude documentation) 
        """
        resp = self.do('gimbal', 'attitude', '?')
        ans = resp.split(' ')
        assert len(ans) == 2, f'get_gimbal_attitude: {resp}'
        return GimbalAttitude(pitch=float(ans[0]), yaw=float(ans[1]))

    def gimbal_push_on(self, attitude_freq: int = 5) -> str:
        """
        Enable a repetitive transmission of the gimbal's attitude at a specified frequency
        

        :param attitude_freq: How often the gimbal attitude is transmitted in Hz (Allowed values: 1, 5, 10, 20, 30, 50)
        :return: ok, or raise certain exception.
        :raise invalid attitude frequency: The attitude frequency you gave was not 1, 5, 10, 20, 30, or 50 Hz

        """
        valid_frequencies = (1, 5, 10, 20, 30, 50)
        assert attitude_freq in valid_frequencies, f'invalid attitude_freq {attitude_freq}'
        resp = self.do('gimbal', 'push', 'attitude', SWITCH_ON, 'afreq', attitude_freq)
        assert self._is_ok(resp), f'gimbal_push_on: {resp}'
        return resp

    def gimbal_push_off(self, attitude: bool = True) -> str:
        """
        Disable the repetitive transmission of the gimbal's attitude at a specified frequency

        :param attitude: if True, disables the transmission of the gimbal's attitude 
        :return: ok, or raise certain exception.
        :raise at least one argument should be True: You just passed the only argument to this function as False, and therefore called this function for no reason
        """
        assert attitude, 'at least one argument should be True'
        resp = self.do('gimbal', 'push', 'attitude', SWITCH_OFF)
        assert self._is_ok(resp), f'gimbal_push_off: {resp}'
        return resp

    def armor_sensitivity(self, value: int) -> str:
        """
        Change the robomaster's armor's sensitivity

        :param value: The sensitivity to set the armor to (range 1 to 10)
        :returns: the robot's response
        :raise value is out of range: The value you gave is out of the sensitivity range of 1 to 10

        """
        assert 1 <= value <= 10, f'value {value} is out of range'
        resp = self.do('armor', 'sensitivity', value)
        assert self._is_ok(resp), f'armor_sensitivity: {resp}'
        return resp

    def get_armor_sensitivity(self) -> int:
        """
        Get the armor sensitivity

        :return: The armor sensitivity
        """
        resp = self.do('armor', 'sensitivity', '?')
        return int(resp)

    def armor_event(self, attr: str, switch: bool) -> str:
        """
        Enable or disable a specified armor event

        :param attr: The name of the armor event, see ARMOR_ENUMS.
        :param switch: True = On, False = Off 
        :return: ok, or raise certain exception.
        :raise unexpected armor event attr: The armor event you gave was not listed in ARMOR_ENUMS
        """
        assert attr in ARMOR_ENUMS, f'unexpected armor event attr {attr}'
        resp = self.do('armor', 'event', attr, SWITCH_ON if switch else SWITCH_OFF)
        assert self._is_ok(resp), f'armor_event: {resp}'
        return resp

    def sound_event(self, attr: str, switch: bool) -> str:
        """
        Enable or disable a specified sound event

        :param attr: The name of the sound event, see SOUND_ENUMS.
        :param switch: True = On, False = Off 
        :return: ok, or raise certain exception.
        :raise unexpected sound event attr: The sound event you gave was not listed in SOUND_ENUMS
        """
        assert attr in SOUND_ENUMS, f'unexpected sound event attr {attr}'
        resp = self.do('sound', 'event', attr, SWITCH_ON if switch else SWITCH_OFF)
        assert self._is_ok(resp), f'sound_event: {resp}'
        return resp

    def led_control(self, comp: str, effect: str, r: int, g: int, b: int) -> str:
        """
        Change the LED effects. Note that the scrolling effect will only work on the gimbal LEDs.

        :param comp: LED ID, this can be an individual LED, or all of them. see LED_ENUMS
        :param effect: The LED effect that the LEDS should perform. see LED_EFFECT_ENUMS
        :param r: RGB red value (range: 0 to 255)
        :param g: RGB green value (range: 0 to 255)
        :param b: RGB blue value (range: 0 to 255)
        :return: ok, or raise certain exception.
        :raise unknown comp: The LED ID you gave for comp was not in the list of LED_ENUMS
        :raise unknown effect: The effect you gave was not in the list of LED_EFFECT_ENUMS
        :raise r is out of range: The red value you gave was not in the range of 0 to 255
        :raise g is out of range: The green value you gave was not in the range of 0 to 255
        :raise b is out of range: The blue value you gave was not in the range of 0 to 255
        :raise scrolling effect works only on gimbal LEDs: You tried to set an armor LED to scroll
        """
        assert comp in LED_ENUMS, f'unknown comp {comp}'
        assert effect in LED_EFFECT_ENUMS, f'unknown effect {effect}'
        assert 0 <= r <= 255, f'r {r} is out of range'
        assert 0 <= g <= 255, f'g {g} is out of range'
        assert 0 <= b <= 255, f'b {b} is out of range'
        if effect == LED_EFFECT_SCROLLING:
            assert comp in (LED_TOP_ALL, LED_TOP_LEFT, LED_TOP_RIGHT), 'scrolling effect works only on gimbal LEDs'
        resp = self.do('led', 'control', 'comp', comp, 'r', r, 'g', g, 'b', b, 'effect', effect)
        assert self._is_ok(resp), f'led_control: {resp}'
        return resp

    def ir_sensor_measure(self, switch: bool = True):
        """
        Enable or disable all of the IR sensors. (Robomaster EP Only)

        :param switch: True = On, False = Off
        :return:ok, or raise certain exception.
        """
        resp = self.do('ir_distance_sensor', 'measure', SWITCH_ON if switch else SWITCH_OFF)
        assert self._is_ok(resp), f'ir_sensor_measure: {resp}'
        return resp

    def get_ir_sensor_distance(self, id: int) -> float:
        """
        Get the distance measured by a specified IR sensor (Robomaster EP Only)

        :param id: ID of IR sensor (range 1 to 4)
        :return: The distance measured in mm
        :raise invalid IR sensor id: The sensor ID you gave is out of the range of 1 to 4
        """
        assert 1 <= id <= 4, f'invalid IR sensor id {id}'
        resp = self.do('ir_distance_sensor', 'distance', id, '?')
        return float(resp)

    def stream(self, switch: bool) -> str:
        """
        Enable or disable the video stream

        :param switch: True = enable, False = disable
        :return: ok, or raise certain exception.
        """
        resp = self.do('stream', SWITCH_ON if switch else SWITCH_OFF)
        assert self._is_ok(resp), f'stream: {resp}'
        return resp

    def audio(self, switch: bool) -> str:
        """
        Enable or disable audio stream.

        :param switch: True = enable, False = disable
        :return: ok, or raise certain exception.
        """
        resp = self.do('audio', SWITCH_ON if switch else SWITCH_OFF)
        assert self._is_ok(resp), f'audio: {resp}'
        return resp
    
    def set_blaster_burst_number(self, beadNumber: int) -> str:
        """
        Set the number of beads fired in one burst of the blaster

        :param beadNumber: The number of beads to fire in one burst (range: 1 to 5)
        :return: The robot's response
        :raise beadNumber is out of range: The number of beads you gave is out of range of 1 to 5
        """

        assert 1 <= beadNumber <= 5, f'beadNumber {beadNumber} is out of range'
        resp = self.do('blaster', 'bead', beadNumber)
        assert self._is_ok(resp), f'{resp}'
        return resp

    def get_blaster_burst_number(self) -> str:
        """
        Get the number of beads fired in one burst of the blaster

        :return: The robot's response
        """

        resp = self.do('blaster', 'bead', '?')
        return resp

    def blaster_fire(self) -> str:
        """
        Fire the blaster in one burst

        :return: ok, or raise certain exception.
        """
        resp = self.do('blaster', 'fire')
        assert self._is_ok(resp), f'blaster_fire: {resp}'
        return resp
