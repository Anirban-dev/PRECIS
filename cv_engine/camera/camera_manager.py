from cv_engine.camera.camera_stream import CameraStream


class CameraManager:

    def __init__(self):

        self.cameras = {}

    def register_camera(
        self,
        camera_id,
        source
    ):

        if camera_id in self.cameras:

            return {
                "success": False,
                "message": "Camera already exists"
            }

        self.cameras[camera_id] = CameraStream(
            source
        )

        return {
            "success": True,
            "camera_id": camera_id,
            "source": source
        }

    def get_camera(
        self,
        camera_id
    ):

        return self.cameras.get(
            camera_id
        )

    def list_cameras(self):

        return {
            "count": len(self.cameras),
            "cameras": list(
                self.cameras.keys()
            )
        }

    def remove_camera(
        self,
        camera_id
    ):

        if camera_id not in self.cameras:

            return {
                "success": False,
                "message": "Camera not found"
            }

        del self.cameras[camera_id]

        return {
            "success": True,
            "camera_id": camera_id
        }

    def start_camera(
        self,
        camera_id
    ):

        camera = self.get_camera(
            camera_id
        )

        if camera is None:

            return {
                "success": False,
                "message": "Camera not found"
            }

        return {
            "success": True,
            "message": f"{camera_id} ready"
        }