import json

def parse_rotation(context, snapshot):
    context.save('rotation.json', json.dumps(dict(
        x = snapshot.pose.rotation.x,
        y = snapshot.pose.rotation.y,
        z = snapshot.pose.rotation.z,
        w = snapshot.pose.rotation.w,
    )))
parse_rotation.field = 'rotation'