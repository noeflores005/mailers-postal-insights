"""Optional local preview server. No third-party packages required."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from pathlib import Path
import argparse,webbrowser
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8766);p.add_argument('--no-browser',action='store_true');a=p.parse_args()
 server=ThreadingHTTPServer(('127.0.0.1',a.port),partial(SimpleHTTPRequestHandler,directory=str(Path(__file__).resolve().parent)))
 url=f'http://127.0.0.1:{a.port}/index.html';print('Mailers:',url,'; Ctrl+C stops the server.')
 if not a.no_browser:webbrowser.open(url)
 try:server.serve_forever()
 except KeyboardInterrupt:server.server_close()
