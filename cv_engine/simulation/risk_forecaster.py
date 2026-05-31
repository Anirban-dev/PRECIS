from cv_engine.simulation.pressure_propagation import (
    PressurePropagation
)

from cv_engine.simulation.crowd_flow_simulator import (
    CrowdFlowSimulator
)


class RiskForecaster:

    def __init__(self):

        self.pressure = (
            PressurePropagation()
        )

        self.simulator = (
            CrowdFlowSimulator()
        )

    def forecast(

        self,

        density_map,

        flow_vectors
    ):

        future_density = (

            self.simulator.simulate(

                density_map,

                flow_vectors
            )
        )

        pressure_score = (

            self.pressure.calculate(
                future_density
            )
        )

        risk_level = (

            self.pressure.classify(
                pressure_score
            )
        )

        return {

            "future_density":
                future_density,

            "pressure_score":
                pressure_score,

            "forecast_risk":
                risk_level
        }