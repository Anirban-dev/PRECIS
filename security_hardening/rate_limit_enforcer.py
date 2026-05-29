class RateLimitEnforcer:

    def allowed(

        self,

        request_count
    ):

        return request_count < 1000