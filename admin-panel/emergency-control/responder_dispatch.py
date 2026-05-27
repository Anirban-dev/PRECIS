from datetime import datetime


class ResponderDispatch:

    def dispatch_units(self):

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "responders_active": 14,

            "ambulances": 3,

            "police_units": 5
        }