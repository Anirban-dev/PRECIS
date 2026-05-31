class CleanupWorker:

    def cleanup(

        self,

        records
    ):

        return [

            record

            for record in records

            if record is not None
        ]