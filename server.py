#!/usr/bin/env python3

import socket
from http import Request
from handlers import RequestHandler


def start_server(handler: RequestHandler):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 8080))
    server_socket.listen(1)

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        request = client_socket.recv(1024).decode('utf-8')
        parsed_request = parse_request(request)
        print(f"Received request: {parsed_request}")
        response = handler(parsed_request)  # Call the handler like a function
        client_socket.sendall(response.to_bytes())
        client_socket.close()
    
def parse_request(request: str) -> Request:
    request_lines, body = request.split('\r\n\r\n')
    request_lines = request_lines.split('\r\n')

    method, path, _ = request_lines[0].split(' ')
    headers = {}
    for line in request_lines[1:]:
        if line == '':
            break
        key, value = line.split(': ')
        headers[key] = value
    return Request(method, path, headers, body)

if __name__ == "__main__":
    start_server(RequestHandler())