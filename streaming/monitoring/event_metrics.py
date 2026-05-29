class EventMetrics:

    def __init__(self):

        self.events_processed = 0

    def increment(self):

        self.events_processed += 1

    def metrics(self):

        return {

            "events_processed":
                self.events_processed
        }