import os
import re

from http import Request, Response
from typing import Callable, List, Tuple, Pattern



class RequestHandler:
    def __init__(self):
        self.routes: List[Tuple[Pattern, Callable]] = [
            (re.compile(r'^/$'), self.home),
            (re.compile(r'^/(.*)$'), self.serve_static_file)
        ]
        self.files = get_directory_files('./www')

    def __call__(self, request: Request) -> Response:
        for pattern, handler in self.routes:
            match = pattern.match(request.path)
            if match:
                return handler(request)
        
        return self.not_found(request)
    
    def home(self, request: Request) -> Response:
        with open('www/index.html', 'rb') as file:
            content = file.read()
            return Response(200, {'Content-Type': 'text/html'}, content.decode('utf-8'))

    def serve_static_file(self, request: Request) -> Response:
        file_path = request.path.split('/')[-1]
        if file_path not in self.files:
            return self.not_found(request)
        
        with open(f'www/{file_path}', 'rb') as file:
            content = file.read()
            content_type = get_content_type(file_path)
            if content_type.startswith('text/'):
                content = content.decode('utf-8')
            return Response(200, {'Content-Type': content_type}, content)

    def not_found(self, request: Request) -> Response:
        return Response(404, {'Content-Type': 'text/html'}, '<h1>404 Not Found</h1>') 

def get_directory_files(folder: str) -> List[str]:
    try:
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        return files
    except Exception as e:
        return []

def get_content_type(file_name: str) -> str:
    extension = os.path.splitext(file_name)[1]
    if extension == '.html':
        return 'text/html'
    elif extension == '.css':
        return 'text/css'
    elif extension == '.png':
        return 'image/png'
    elif extension == '.jpg':
        return 'image/jpeg'
        