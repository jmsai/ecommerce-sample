class ErrorView:
    def display(self, error):
        return {
            "title": error.title,
            "message": error.message,
            "code": error.code
        }
