import subprocess
import sys

from backend.services.camera_registry import (
    CameraRegistry
)

from cv_engine.camera.camera_manager import (
    CameraManager
)


class CameraService:

    def __init__(self):

        self.process = None

        self.registry = CameraRegistry()

        self.manager = CameraManager()

    def start_camera(
        self,
        camera_id
    ):

        camera = self.registry.get(
            camera_id
        )

        if camera is None:

            return {
                "success": False,
                "message": "Camera not registered"
            }

        source = camera["stream_url"]

        self.manager.register_camera(
            camera_id,
            source
        )

        if self.process:

            if self.process.poll() is None:

                return {
                    "success": False,
                    "message": "Camera already running"
                }

        self.process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "cv_engine.camera.camera_stream"
            ]
        )

        return {
            "success": True,
            "camera_id": camera_id,
            "source": source,
            "pid": self.process.pid
        }

    def stop(self):

        if not self.process:

            return {
                "success": False,
                "message": "Camera not running"
            }

        if self.process.poll() is None:

            self.process.terminate()

        self.process = None

        return {
            "success": True,
            "message": "Camera stopped"
        }

    def status(self):

        running = (

            self.process is not None

            and

            self.process.poll() is None
        )

        return {
            "running": running,
            "pid":
                self.process.pid
                if running
                else None
        }