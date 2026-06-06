from system_integration.predictive_pipeline import (
    PredictivePipeline
)


def test_pipeline():

    pipeline = PredictivePipeline()

    result = pipeline.execute(

        rgb_density=[10, 20, 30],

        thermal_density=[12, 18, 28],

        infrared_density=[11, 19, 27],

        flow_vectors=[
            [1, 0],
            [0, 1]
        ],

        turbulence_score=10
    )

    print(result)

    assert result is not None