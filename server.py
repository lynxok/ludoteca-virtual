import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

class UploadHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/upload':
            query = urllib.parse.parse_qs(parsed_path.query)
            if 'filename' in query:
                filename = query['filename'][0]
                # Ensure the filename is safe and goes to portadas/
                filename = os.path.basename(filename)
                
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    file_data = self.rfile.read(content_length)
                    
                    if not os.path.exists('portadas'):
                        os.makedirs('portadas')
                        
                    filepath = os.path.join('portadas', filename)
                    with open(filepath, 'wb') as f:
                        f.write(file_data)
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status":"success"}')
                    return
        
        self.send_response(400)
        self.end_headers()

if __name__ == '__main__':
    port = 7560
    server = HTTPServer(('127.0.0.1', port), UploadHandler)
    print(f"Server listening on port {port}...")
    server.serve_forever()
