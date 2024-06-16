import io
import os
import socket
import struct
import threading
import time
from time import sleep
from typing import Any, Callable, Optional, Tuple, Union

import av
import cv2
import numpy as np
from adbutils import AdbConnection, AdbDevice, AdbError, Network, adb
from av.packet import Packet
from av.codec import CodecContext
from av.error import InvalidDataError

from .const import (
    EVENT_DISCONNECT ,
    EVENT_FRAME ,
    EVENT_INIT ,
    LOCK_SCREEN_ORIENTATION_UNLOCKED , Recording_mode  ,
)
from .control import ControlSender

#from demuxer.c
SC_PACKET_FLAG_CONFIG = 1 << 63
SC_PACKET_FLAG_KEY_FRAME = 1 << 62
SC_PACKET_PTS_MASK = SC_PACKET_FLAG_KEY_FRAME - 1

#from av/ffmpeg ==> needs to check in python av
AV_NOPTS_VALUE = 0x8000000000000000
AV_PKT_FLAG_KEY=   0x0001

from enum import Enum , auto


class Codec(Enum) :
    SC_CODEC_H264= auto()




class Client:
    def __init__(
        self,
        device: Optional[Union[AdbDevice, str, any]] = None,
        max_width: int = 0,
        bitrate: int = 8000000,
        max_fps: int = 0,
        flip: bool = False,
        block_frame: bool = False,
        stay_awake: bool = False,
        lock_screen_orientation: int = LOCK_SCREEN_ORIENTATION_UNLOCKED,
        connection_timeout: int = 3000,
        encoder_name: Optional[str] = None,
        recording_mode: Optional[Recording_mode] = Recording_mode.NO_AUDIO,
    ):
        """
        Create a scrcpy client, this client won't be started until you call the start function

        Args:
            device: Android device, select first one if none, from serial if str
            max_width: frame width that will be broadcast from android server
            bitrate: bitrate
            max_fps: maximum fps, 0 means not limited (supported after android 10)
            flip: flip the video
            block_frame: only return nonempty frames, may block cv2 render thread
            stay_awake: keep Android device awake
            lock_screen_orientation: lock screen orientation, LOCK_SCREEN_ORIENTATION_*
            connection_timeout: timeout for connection, unit is ms
            encoder_name: encoder name, enum: [OMX.google.h264.encoder, OMX.qcom.video.encoder.avc, c2.qti.avc.encoder, c2.android.avc.encoder], default is None (Auto)
        """
        # Check Params
        assert max_width >= 0, "max_width must be greater than or equal to 0"
        assert bitrate >= 0, "bitrate must be greater than or equal to 0"
        assert max_fps >= 0, "max_fps must be greater than or equal to 0"
        assert (
            -1 <= lock_screen_orientation <= 3
        ), "lock_screen_orientation must be LOCK_SCREEN_ORIENTATION_*"
        assert (
            connection_timeout >= 0
        ), "connection_timeout must be greater than or equal to 0"
        assert encoder_name in [
            None,
            "OMX.google.h264.encoder",
            "OMX.qcom.video.encoder.avc",
            "c2.qti.avc.encoder",
            "c2.android.avc.encoder",
        ]

        # Params
        self.flip = flip
        self.max_width = max_width
        self.bitrate = bitrate
        self.max_fps = max_fps
        self.block_frame = block_frame
        self.stay_awake = stay_awake
        self.lock_screen_orientation = lock_screen_orientation
        self.connection_timeout = connection_timeout
        self.encoder_name = encoder_name

        #received from server
        self.codec = None

        # Connect to device
        if device is None:
            device = adb.device_list()[0]
        elif isinstance(device, str):
            device = adb.device(serial=device)

        self.device = device
        self.listeners = dict(frame=[], init=[], disconnect=[])

        # User accessible
        self.last_frame: Optional[np.ndarray] = None
        self.resolution: Optional[Tuple[int, int]] = None
        self.device_name: Optional[str] = None
        self.control = ControlSender(self)

        self.recording_mode = recording_mode

        # Need to destroy
        self.alive = False
        self.__server_stream: Optional[AdbConnection] = None
        self.__video_socket: Optional[socket.socket] = None
        self.control_socket: Optional[socket.socket] = None
        self.control_socket_lock = threading.Lock()

        # Available if start with threaded or daemon_threaded
        self.stream_loop_thread = None

    def __init_server_connection(self) -> None:
        """
        Connect to android server, there will be two sockets, video and control socket.
        This method will set: video_socket, control_socket, resolution variables
        """


        if self.recording_mode != Recording_mode.NO_VIDEO:
            for _ in range(self.connection_timeout // 100):
                try:
                    self.__video_socket = self.device.create_connection(
                        Network.LOCAL_ABSTRACT, "scrcpy"
                    )
                    break
                except AdbError:
                    sleep(0.1)
                    pass
            else:
                raise ConnectionError("Failed to connect scrcpy-server after 3 seconds")

            self.control_socket = self.device.create_connection (
                Network.LOCAL_ABSTRACT , "scrcpy"
            )

            self.control_socket = self.device.create_connection (
                Network.LOCAL_ABSTRACT , "scrcpy"
            )

            dummy_byte = self.__video_socket.recv(1)
            if not len(dummy_byte) or dummy_byte != b"\x00":
                raise ConnectionError("Did not receive Dummy Byte!")


            self.device_name = self.__video_socket.recv(64).decode("utf-8").rstrip("\x00")
            if not len(self.device_name):
                raise ConnectionError("Did not receive Device Name!")

            codec = self.__video_socket.recv(4)
            self.codec  = codec.decode("utf-8")
            self.__video_socket.setblocking(False)

        if self.recording_mode != Recording_mode.NO_AUDIO:
            for _ in range ( self.connection_timeout // 100 ) :
                try :
                    self.__audio_socket = self.device.create_connection (
                        Network.LOCAL_ABSTRACT , "scrcpy"
                    )
                    break
                except AdbError :
                    sleep ( 0.1 )
                    pass
            else :
                raise ConnectionError ( "Failed to connect scrcpy-server after 3 seconds" )

            self.control_socket = self.device.create_connection (
                Network.LOCAL_ABSTRACT , "scrcpy"
            )

            dummy_byte = self.__audio_socket.recv ( 1 )
            if not len ( dummy_byte ) or dummy_byte != b"\x00" :
                raise ConnectionError ( "Did not receive Dummy Byte!" )

            header = self.__audio_socket.recv ( 64 )

            self.device_name = header.decode ( "utf-8" ).rstrip ( "\x00" )
            if not len ( self.device_name ) :
                raise ConnectionError ( "Did not receive Device Name!" )
            codec = self.__audio_socket.recv ( 4 )
            self.codec = codec.decode("utf-8")
            #self.__audio_socket.setblocking ( False )



    def __deploy_server(self) -> None:
        """
        Deploy server to android device
        """
        jar_name = "scrcpy-server.jar"
        server_file_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), jar_name
        )
        self.device.sync.push(server_file_path, f"/data/local/tmp/{jar_name}")
        if (self.recording_mode == Recording_mode.NO_AUDIO):
            commands = [
                f"CLASSPATH=/data/local/tmp/{jar_name}",
                "app_process",
                "/",
                "com.genymobile.scrcpy.Server",
                "2.4",  # Scrcpy server version
                "log_level=info",
                f"max_size={self.max_width}",
                f"max_fps={self.max_fps}",
                f"video_bit_rate={self.bitrate}",
                "tunnel_forward=true",
                "send_frame_meta=false",
                "control=true",
                "audio=false",
                "show_touches=false",
                "stay_awake=false",
                "power_off_on_close=false",
                "clipboard_autosync=false"
            ]
        elif (self.recording_mode == Recording_mode.NO_VIDEO):
            commands = [
                f"CLASSPATH=/data/local/tmp/{jar_name}" ,
                "app_process" ,
                "/" ,
                "com.genymobile.scrcpy.Server" ,
                "2.4" ,  # Scrcpy server version
                "log_level=info" ,
                "tunnel_forward=true" ,
                "send_frame_meta=true" ,
                "control=true" ,
                "audio=true" ,
                "audio_codec=flac",
                "video=false",
                "show_touches=false" ,
                "stay_awake=false" ,
                "power_off_on_close=false" ,
                "clipboard_autosync=false"
            ]

        self.__server_stream: AdbConnection = self.device.shell(
            commands,
            stream=True,
        )

        # Wait for server to start
        self.__server_stream.read(10)

    def start(self, threaded: bool = False, daemon_threaded: bool = False) -> None:
        """
        Start listening video stream

        Args:
            threaded: Run stream loop in a different thread to avoid blocking
            daemon_threaded: Run stream loop in a daemon thread to avoid blocking
        """
        assert self.alive is False

        self.__deploy_server()
        self.__init_server_connection()
        self.alive = True
        self.__send_to_listeners(EVENT_INIT)

        if threaded or daemon_threaded:
            self.stream_loop_thread = threading.Thread(
                target=self.__stream_loop, daemon=daemon_threaded
            )
            self.stream_loop_thread.start()
        else:
            self.__stream_loop()

    def stop(self) -> None:
        """
        Stop listening (both threaded and blocked)
        """
        self.alive = False
        if self.__server_stream is not None:
            try:
                self.__server_stream.close()
            except Exception:
                pass

        if self.control_socket is not None:
            try:
                self.control_socket.close()
            except Exception:
                pass

        if self.__video_socket is not None:
            try:
                self.__video_socket.close()
            except Exception:
                pass

    def __stream_loop(self) -> None:
        """
        Core loop for video parsing
        """
        codec = CodecContext.create(codec = self.codec, mode =  "r")




        while self.alive:
            if self.recording_mode != Recording_mode.NO_VIDEO:
                try:
                    raw_h264 = self.__video_socket.recv(0x10000)
                    if raw_h264 == b"":
                        raise ConnectionError("Video stream is disconnected")
                    packets = codec.parse(raw_h264)
                    for packet in packets:
                        frames = codec.decode(packet)
                        for frame in frames:
                            frame = frame.to_ndarray(format="bgr24")
                            if self.flip:
                                frame = cv2.flip(frame, 1)
                            self.last_frame = frame
                            self.resolution = (frame.shape[1], frame.shape[0])
                            self.__send_to_listeners(EVENT_FRAME, frame)
                except (BlockingIOError, InvalidDataError):
                    time.sleep(0.01)
                    if not self.block_frame:
                        self.__send_to_listeners(EVENT_FRAME, None)
                except (ConnectionError, OSError) as e:  # Socket Closed
                    if self.alive:
                        self.__send_to_listeners(EVENT_DISCONNECT)
                        self.stop()
                        raise e
            elif self.recording_mode == Recording_mode.NO_VIDEO :
                try:
                    windows_size = 30
                    packets = []
                    while(windows_size > 0 and self.alive):
                        pts_header_buffer =  self.__audio_socket.recv ( 8 )
                        if pts_header_buffer == b"" :
                            raise ConnectionError ( "Audio stream is disconnected" )

                        pts_flags = struct.unpack(">Q", pts_header_buffer)

                        #if (pts_flags & SC_PACKET_FLAG_CONFIG) :
                        #    pts = AV_NOPTS_VALUE
                        #else:
                        #    pts = pts_flags & SC_PACKET_PTS_MASK

                        #if (pts_flags & SC_PACKET_FLAG_KEY_FRAME) :
                        #    flags = flags | AV_PKT_FLAG_KEY

                        len_packet_byte_val =  self.__audio_socket.recv ( 4 )
                        len_packet = int.from_bytes ( len_packet_byte_val , "big" )

                        packet_buffer =  self.__audio_socket.recv ( len_packet )
                        packets_in_window = codec.parse(packet_buffer)
                        packets = packets + packets_in_window
                        windows_size -=1


                    self.__send_to_listeners ( EVENT_FRAME , packets )

                except (BlockingIOError , InvalidDataError):
                    time.sleep ( 0.01 )
                    #need to bufferize

                except (ConnectionError , OSError) as e:  # Socket Closed
                    if self.alive :
                        self.__send_to_listeners ( EVENT_DISCONNECT )
                        self.stop ()
                        raise e

    def add_listener(self, cls: str, listener: Callable[..., Any]) -> None:
        """
        Add a video listener

        Args:
            cls: Listener category, support: init, frame
            listener: A function to receive frame np.ndarray
        """
        self.listeners[cls].append(listener)

    def remove_listener(self, cls: str, listener: Callable[..., Any]) -> None:
        """
        Remove a video listener

        Args:
            cls: Listener category, support: init, frame
            listener: A function to receive frame np.ndarray
        """
        self.listeners[cls].remove(listener)

    def __send_to_listeners(self, cls: str, *args, **kwargs) -> None:
        """
        Send event to listeners

        Args:
            cls: Listener type
            *args: Other arguments
            *kwargs: Other arguments
        """
        for fun in self.listeners[cls]:
            fun(*args, **kwargs)

    def codec_handler(self, codec_str):

         match (codec_str) :
                case "h264":
                    return Codec.SC_CODEC_H264
                case "h265" :
                    return Codec.SC_CODEC_H265
                case "av1":
                    return Codec.SC_CODEC_AV1
                case "opus":
                    return Codec.SC_CODEC_OPUS
                case "aac" :
                    return Codec.SC_CODEC_AAC
                case "flac":
                    return Codec.SC_CODEC_FLAC
                case  "raw":
                    return Codec.SC_CODEC_RAW
                case _:
                    raise Exception(f'Unknown code {codec_str}' )
