class CameraRegistry:
    def __init__(self):
        self.registry = {}

    def register(self, camera_id, stream_url, sector_id, camera_type):
        self.registry[camera_id] = {
            "camera_id": camera_id,
            "stream_url": stream_url,
            "sector_id": sector_id,
            "camera_type": camera_type,
            "status": "REGISTERED"
        }
        return self.registry[camera_id]

    def get(self, camera_id):
        return self.registry.get(camera_id)

    def all(self):
        return {
            "count": len(self.registry),
            "cameras": list(self.registry.values())
        }

    def remove(self, camera_id):
        if camera_id not in self.registry:
            return False

        del self.registry[camera_id]
        return True
