from pathlib import Path 

class Context:
    def __init__(self, dir_name):
        """
        dir_name - a PosixPath object, OR a string.
        self.dir- the same PosixPath object.
        self.dir_string- a simple string representing the path.
        """
        if isinstance(dir_name, str):
            self.dir = Path(dir_name)
            self.dir_string = dir_name
        else: #if it's a PosixPath
            self.dir = dir_name
            self.dir_string = dir_name.absolute().as_posix()
    def make_dir(self):
        os.makedirs(self.dir, exist_ok=True)
    def path(self, filename):
        return self.dir / filename
    def save(self, filename, string=""):
        """create a new file with the given filename, and put in it the given string.
        If no string parameter is given, create a new empty file."""
        open_fmt = 'wb+' if isinstance(string, bytes) else 'w+'        
        with open(self.dir / filename, open_fmt) as f:
            f.write(string)

def context_from_snapshot(snapshot):
    """
    given a json string representing a snapshot, return a Context object of the dir.
    """
    snap_dict = json.loads(snapshot)
    return Context(snap_dict['snapshot_dir'])