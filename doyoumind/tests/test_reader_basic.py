import time

from do_you_mind.doyoumind import Reader

path = "/home/user/Downloads/sample.mind"
read = Reader(path, zipped=False)
user = read.user
print(user.user_id, user.username, user.birthdate, user.gender)
for snap in read:
    #print(snap.timestamp, snap.color_image, snap.depth_image, snap.user_feelings)
    #snap.color_image.show()
    #snap.depth_image.show()

print("done!")