from dataclasses import dataclass


@dataclass
class HTTPErrorCodes:
    code: int
    message: str

    codes = {
        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        408: "Request Timeout",
        422: "Unprocessable Entity",
        500: "Internal Server Error",
    }

    def get_status(self, code):
        return self.codes[code]
