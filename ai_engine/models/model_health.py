from pathlib import Path


class ModelHealth:

    def check(

        self,

        model_path
    ):

        path = Path(model_path)

        return {

            "exists":
                path.exists(),

            "size_mb":

                round(
                    path.stat().st_size /
                    1024 /
                    1024,
                    2
                )

                if path.exists()

                else 0
        }