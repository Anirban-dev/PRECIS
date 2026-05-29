import time


class RetryEngine:

    def execute(
        self,
        function,
        retries=3
    ):

        for _ in range(retries):

            try:

                return function()

            except Exception:

                time.sleep(1)

        return None