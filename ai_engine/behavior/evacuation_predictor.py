class EvacuationPredictor:

    def estimate_time(

        self,

        crowd_size,

        exit_capacity
    ):

        if exit_capacity <= 0:

            return None

        return round(

            crowd_size /

            exit_capacity,

            2
        )

    def evacuation_status(

        self,

        crowd_size,

        exit_capacity
    ):

        time_required = (

            self.estimate_time(

                crowd_size,

                exit_capacity
            )
        )

        if time_required is None:

            return "BLOCKED"

        if time_required > 20:

            return "CRITICAL"

        if time_required > 10:

            return "HIGH"

        return "NORMAL"