import numpy as np


class CrowdFlowClassifier:

    def classify(

        self,

        flow_vectors
    ):

        if len(flow_vectors) == 0:

            return "UNKNOWN"

        vectors = np.array(
            flow_vectors
        )

        mean_x = np.mean(
            vectors[:, 0]
        )

        mean_y = np.mean(
            vectors[:, 1]
        )

        if abs(mean_x) > abs(mean_y):

            return "HORIZONTAL"

        if abs(mean_y) > abs(mean_x):

            return "VERTICAL"

        return "MIXED"

    def confidence(

        self,

        flow_vectors
    ):

        if len(flow_vectors) == 0:

            return 0.0

        return min(

            len(flow_vectors) / 100,

            1.0
        )