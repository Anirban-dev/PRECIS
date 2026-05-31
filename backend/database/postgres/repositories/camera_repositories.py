class CameraRepository:

    def create_camera(

        self,

        payload
    ):

        return {

            "status":
                "CREATED",

            "camera":
                payload
        }

    def get_camera(

        self,

        camera_id
    ):

        return {

            "camera_id":
                camera_id
        }

    def update_health(

        self,

        camera_id,

        health
    ):

        return {

            "camera_id":
                camera_id,

            "health":
                health
        }