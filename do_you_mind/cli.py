import sys
import inspect
class CommandLineInterface:

	def __init__(self):
		self.interface_funcs = {}

	def command(self, f):
		self.interface_funcs[f.__name__] = f
		return f

	def main(self):
		USAGE_MSG = "USAGE: python example.py <command> [<key>=<value>]*"
		#we don't need the list args here,
		#as the user only gives keywords,
		#but we're leaving it here to make it 
		#more intuitive.
		args = []
		kwargs = {}

		try:
			func_name = sys.argv[1]
			if func_name not in self.interface_funcs:
				raise Exception
			else:
				f = self.interface_funcs[func_name]
			
			#check if the arguments match the function's signature
			for user_arg in sys.argv[2:]:
				key, value = user_arg.split("=")
				kwargs[key] = value
				
			inspect.getcallargs(f, *args, **kwargs)

		#we got an exception if there was incorrect format
		except Exception:
			print(USAGE_MSG)
			sys.exit(1)

		return f(*args, **kwargs)



        
