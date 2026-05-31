from datetime import datetime


class DigitalTwin:

    def create_snapshot(

        self,

        sector_id,

        density,

        risk_level
    ):

        return {

            "sector_id":
                sector_id,

            "density":
                density,

            "risk_level":
                risk_level,

            "timestamp":
                datetime.utcnow().isoformat()
        }

    def update(

        self,

        twin_state,

        updates
    ):

        twin_state.update(
            updates
        )

        return twin_state