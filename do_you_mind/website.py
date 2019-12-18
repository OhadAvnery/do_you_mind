import functools
import http.server
import re

def Handler_class_factory(path_to_handler):
	class Handler(http.server.BaseHTTPRequestHandler):
			def do_GET(self):
				func = None
				for path_pattern in path_to_handler:
					match = re.match(path_pattern, self.path)
					if match:
						match_args = match.groups()
						func = path_to_handler[path_pattern]
						status, status_body = func(*match_args)
						self.send_response(status)
						self.send_header("Content-type", "text/html")
						self.end_headers()
						self.wfile.write(bytes(status_body, "utf-8"))
						break
				if not func:
					self.send_response(404)
					self.send_header("Content-type", "text/html")
					self.end_headers()
					self.wfile.write(b'')

	return Handler

class Website:
	"""
	path_to_handler- a dictionary.
	its keys- paths given as strings (perhaps with regex).
	values- handlers that should work on the given path.
	"""
	def __init__(self):
		self.__path_to_handler = {}
	
	def route(self, path):
		def decorator(f):
			nonlocal path
			#we won't use a wrapper here, as we don't need to change f
			
			#force path to start with ^ and end with $, so that it only matches complete strings
			if path[0] != '^':
				path = '^'+path
			if path[-1] != '$':
				path += '$'

			self.__path_to_handler[path] = f
			return f
	

		return decorator

	def run(self, address):
		Handler = Handler_class_factory(self.__path_to_handler)

		hostName, serverPort = address
		webServer = http.server.HTTPServer((hostName, serverPort), Handler)

		try:
			webServer.serve_forever()
		except KeyboardInterrupt:
			pass

		webServer.server_close()