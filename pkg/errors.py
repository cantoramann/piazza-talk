class InvalidPostError(Exception):
    """Exception raised for errors in the input post."""

    def __init__(self, post_id, message="Post may be violating publicity rules."):
        self.post_id = post_id
        self.message = message
        super().__init__(f"Error in post {post_id}: {message}")