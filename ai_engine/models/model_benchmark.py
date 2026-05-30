import time


class Benchmark:

    def measure(

        self,

        function,
        *args,
        **kwargs
    ):

        start = time.time()

        result = function(
            *args,
            **kwargs
        )

        end = time.time()

        return {

            "result":
                result,

            "latency_ms":

                round(
                    (end - start) *
                    1000,
                    2
                )
        }