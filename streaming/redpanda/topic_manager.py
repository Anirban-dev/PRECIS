class TopicManager:

    def create_topic(
        self,
        topic_name
    ):

        return {
            "topic": topic_name,
            "status": "CREATED"
        }

    def delete_topic(
        self,
        topic_name
    ):

        return {
            "topic": topic_name,
            "status": "DELETED"
        }