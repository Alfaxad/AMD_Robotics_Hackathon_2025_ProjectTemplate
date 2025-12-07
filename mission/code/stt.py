#!/usr/bin/env python3  
"""  
Voice-controlled robot using Whisper STT and LeRobot.  
Configured for SO101 follower with top and side cameras.  
"""  
  
import asyncio  
import logging  
import queue  
import threading  
from dataclasses import dataclass  
from typing import Dict, Any, Optional  
  
import numpy as np  
import torch  
import whisper  
from lerobot.robots import make_robot_from_config  
from lerobot.robots.configs import RobotConfig  
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig  
  
@dataclass  
class VoiceCommandConfig:  
    """Configuration for voice-controlled robot."""  
    # Robot configuration - using your specific setup  
    robot_type: str = "so101_follower"  
    robot_port: str = "/dev/ttyACM0"  
    robot_id: str = "my_follower_arm"  
      
    # Camera configuration - matching your setup  
    cameras: Dict[str, OpenCVCameraConfig] = None  
      
    # Whisper configuration  
    whisper_model: str = "base"  
    audio_device: Optional[int] = None  
      
    # Command mapping for SO101 arm  
    command_mappings: Dict[str, Dict[str, Any]] = None  
      
    def __post_init__(self):  
        if self.cameras is None:  
            self.cameras = {  
                "top": OpenCVCameraConfig(  
                    type="opencv",  
                    index_or_path=4,  
                    width=640,  
                    height=480,  
                    fps=30  
                ),  
                "side": OpenCVCameraConfig(  
                    type="opencv",  
                    index_or_path=6,  
                    width=640,  
                    height=480,  
                    fps=30  
                )  
            }  
          
        if self.command_mappings is None:  
            # SO101 uses position control for joints  
            self.command_mappings = {  
                "up": {"shoulder_pan.pos": 0.0, "shoulder_lift.pos": 0.5},  
                "down": {"shoulder_pan.pos": 0.0, "shoulder_lift.pos": -0.5},  
                "left": {"shoulder_pan.pos": -0.5, "shoulder_lift.pos": 0.0},  
                "right": {"shoulder_pan.pos": 0.5, "shoulder_lift.pos": 0.0},  
                "open": {"gripper.pos": 100.0},  
                "close": {"gripper.pos": 0.0},  
                "stop": {joint: 0.0 for joint in [  
                    "shoulder_pan.pos", "shoulder_lift.pos", "elbow_flex.pos",  
                    "wrist_flex.pos", "wrist_roll.pos", "gripper.pos"  
                ]},  
            }  
  
class VoiceRobotController:  
    """Main controller for voice-activated SO101 robot."""  
      
    def __init__(self, config: VoiceCommandConfig):  
        self.config = config  
        self.logger = logging.getLogger(__name__)  
          
        # Initialize Whisper model  
        self.whisper_model = whisper.load_model(config.whisper_model)  
          
        # Initialize robot with cameras  
        self.robot = self._init_robot()  
          
        # Audio processing  
        self.audio_queue = queue.Queue()  
        self.is_running = False  
          
    def _init_robot(self):  
        """Initialize the SO101 robot with cameras."""  
        from lerobot.robots.so101_follower.config_so101_follower import SO101FollowerConfig  
          
        robot_config = SO101FollowerConfig(  
            type=self.config.robot_type,  
            port=self.config.robot_port,  
            id=self.config.robot_id,  
            cameras=self.config.cameras  
        )  
          
        robot = make_robot_from_config(robot_config) [1](#1-0)   
        robot.connect()  
        return robot  
      
    def _capture_audio(self):  
        """Capture audio from microphone in a separate thread."""  
        import speech_recognition as sr  
          
        recognizer = sr.Recognizer()  
        microphone = sr.Microphone(device_index=self.config.audio_device)  
          
        with microphone as source:  
            recognizer.adjust_for_ambient_noise(source)  
              
        while self.is_running:  
            try:  
                self.logger.info("Listening for command...")  
                with microphone as source:  
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)  
                  
                # Convert audio to numpy array for Whisper  
                audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16).astype(np.float32) / 32768.0  
                self.audio_queue.put(audio_data)  
                  
            except sr.WaitTimeoutError:  
                continue  
            except Exception as e:  
                self.logger.error(f"Audio capture error: {e}")  
      
    def _transcribe_audio(self, audio_data: np.ndarray) -> str:  
        """Transcribe audio using Whisper."""  
        try:  
            result = self.whisper_model.transcribe(audio_data, fp16=torch.cuda.is_available())  
            text = result["text"].strip().lower()  
            self.logger.info(f"Transcribed: '{text}'")  
            return text  
        except Exception as e:  
            self.logger.error(f"Transcription error: {e}")  
            return ""  
      
    def _parse_command(self, text: str) -> Optional[Dict[str, Any]]:  
        """Parse transcribed text into robot command."""  
        # Simple keyword matching  
        for command, action in self.config.command_mappings.items():  
            if command in text:  
                return action  
          
        return None  
      
    def _send_action(self, action: Dict[str, Any]):  
        """Send action to SO101 robot."""  
        try:  
            # Filter action to match robot's action features  
            valid_action = {}  
            for key in self.robot.action_features.keys(): [2](#1-1)   
                if key in action:  
                    valid_action[key] = action[key]  
              
            if valid_action:  
                self.robot.send_action(valid_action)  
                self.logger.info(f"Sent action: {valid_action}")  
            else:  
                self.logger.warning(f"No valid actions found for this robot type")  
                  
        except Exception as e:  
            self.logger.error(f"Error sending action: {e}")  
      
    async def run(self):  
        """Main control loop."""  
        self.is_running = True  
          
        # Start audio capture thread  
        audio_thread = threading.Thread(target=self._capture_audio, daemon=True)  
        audio_thread.start()  
          
        self.logger.info("Voice robot controller started. Say 'stop' to exit.")  
          
        try:  
            while self.is_running:  
                try:  
                    # Get audio with timeout  
                    audio_data = self.audio_queue.get(timeout=0.1)  
                      
                    # Transcribe  
                    text = self._transcribe_audio(audio_data)  
                      
                    # Parse command  
                    action = self._parse_command(text)  
                      
                    if action:  
                        # Check for exit command  
                        if "stop" in text and len(text.strip()) == 4:  
                            self.logger.info("Stop command received. Exiting...")  
                            break  
                          
                        # Send action  
                        self._send_action(action)  
                      
                except queue.Empty:  
                    continue  
                except KeyboardInterrupt:  
                    break  
                      
        finally:  
            self.is_running = False  
            self.robot.disconnect()  
            self.logger.info("Voice robot controller stopped")  
  
def main():  
    """Main entry point."""  
    logging.basicConfig(level=logging.INFO)  
      
    # Configuration using your specific parameters  
    config = VoiceCommandConfig(  
        robot_type="so101_follower",  
        robot_port="/dev/ttyACM0",  
        robot_id="my_follower_arm",  
        whisper_model="base",  
    )  
      
    # Create and run controller  
    controller = VoiceRobotController(config)  
    asyncio.run(controller.run())  
  
if __name__ == "__main__":  
    main()

