import sys
import http.server
from pathlib import Path
from flask import Flask

website = Flask("do_you_mind")


def run_webserver(host, port, data_dir):
	website.data_dir = data_dir
	website.run(host, port)


@website.route('/')
def index():
	_INDEX_HTML = '''
		<html>
	<head>
		<title>Brain Computer Interface</title>
	</head>
	<body>
		<ul>
			{users}
		</ul>
	</body>
</html>
	'''

	_USER_LINE_HTML = '''
	<li><a href="/users/{user_id}">user {user_id}</a></li>
	'''
	users_html = []

	data_path_obj = Path(website.data_dir)

	user_id_list = [user_dir.name for user_dir in data_path_obj.iterdir()]

	for user_id in user_id_list:
		users_html.append(_USER_LINE_HTML.format(user_id=user_id))
	index_html = _INDEX_HTML.format(users='\n'.join(users_html))
	#return 200, index_html
	return index_html

@website.route('/users/<user_id>')
def user(user_id):
	data_path_obj = Path(website.data_dir)

	user_id_list = [user_dir.name for user_dir in data_path_obj.iterdir()]
	user_path = data_path_obj / user_id
	if user_id not in user_id_list:
		return 404, ''

	_USER_PAGE_HTML = '''
	<html>
	<head>
		<title>Brain Computer Interface: User {user_id}</title>
	</head>
	<body>
		<table>
			{user_thoughts}
		</table>
	</body>
</html>
	'''
	_THOUGHT_LINE_HTML = '''
	<tr>
	<td>{time}</td>
	<td>{thought}</td>
	</tr>
	'''

	thoughts_html = []
	

	for thought_path in user_path.iterdir():
		date, time_in_day = thought_path.stem.split("_")
		time = "{date} {time_in_day}".format(date=date, time_in_day=time_in_day.replace("-",":"))
		thought_file = thought_path.open("r")
		for line in thought_file:
			thoughts_html.append(_THOUGHT_LINE_HTML.format(time=time, thought=line))
		thought_file.close()

	user_page_html = _USER_PAGE_HTML.format(user_id=user_id, user_thoughts='\n'.join(thoughts_html))
	#return 200, user_page_html
	return user_page_html


def main(argv):
	if len(argv) != 3:
		print(f'USAGE: {argv[0]} <ip_address>:<port> <data_dir>')
		return 1
	try:
		address, data_dir = argv[1:]
		host, port = address.split(":")
		#fixed_address = (ip_address, int(port))
		run_webserver(host, int(port), data_dir)
		print('done')
	except Exception as error:
		print(f'ERROR: {error}')
		return 1

if __name__ == '__main__':
	sys.exit(main(sys.argv))
	