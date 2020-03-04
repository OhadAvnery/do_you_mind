from do_you_mind.doyoumind import Reader

path = "/home/user/Downloads/sample.mind"
read = Reader(path, zipped=False)
for snap in read:
    print(snap)