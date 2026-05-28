class DistributedLockManager:

    def acquire_lock(

        self,

        resource
    ):

        return {

            "resource":
                resource,

            "lock":
                "ACQUIRED"
        }