class DetectionMerger:

    def merge(

        self,

        rgb,

        thermal,

        infrared
    ):

        merged = []

        merged.extend(rgb)

        merged.extend(thermal)

        merged.extend(infrared)

        return merged