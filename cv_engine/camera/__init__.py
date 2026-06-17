def __init__(

    self,

    source=0
):

    self.source = source

    self.detector = ThermalDetector()

    self.pipeline = PredictivePipeline()