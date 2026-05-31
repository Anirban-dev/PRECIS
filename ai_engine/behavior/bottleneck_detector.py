class BottleneckDetector:

    def detect(

        self,

        entry_rate,

        exit_rate
    ):

        if exit_rate == 0:

            return True

        ratio = entry_rate / exit_rate

        return ratio > 1.5

    def severity(

        self,

        entry_rate,

        exit_rate
    ):

        if exit_rate == 0:

            return "CRITICAL"

        ratio = entry_rate / exit_rate

        if ratio > 3:

            return "CRITICAL"

        if ratio > 2:

            return "HIGH"

        if ratio > 1.5:

            return "MEDIUM"

        return "LOW"