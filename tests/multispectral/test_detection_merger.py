from ai_engine.multispectral.detection_merger import (
    DetectionMerger
)


def test_detection_merge():

    merger = DetectionMerger()

    result = merger.merge(

        rgb=[{"id": 1}],

        thermal=[{"id": 2}],

        infrared=[{"id": 3}]
    )

    assert len(result) == 3