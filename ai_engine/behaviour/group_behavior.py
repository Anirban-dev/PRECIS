class GroupBehavior:

    def evaluate(

        self,

        group_size,

        cohesion
    ):

        if (

            group_size > 20 and

            cohesion > 0.8
        ):

            return "COORDINATED_GROUP"

        if cohesion < 0.3:

            return "DISORDERED_GROUP"

        return "NORMAL_GROUP"