from dataclasses import dataclass


@dataclass
class Request:
    method: str
    path: str
    headers: dict
    body: str


@dataclass
class Response:
    status_code: int
    headers: dict
    body: str

    def to_bytes(self) -> bytes:
        return f"HTTP/1.1 {self.status_code}\r\n".encode('utf-8') + \
            b''.join(f"{key}: {value}\r\n".encode('utf-8') for key, value in self.headers.items()) + \
            b'\r\n' + \
            self.body.encode('utf-8') if type(self.body) == str else self.body