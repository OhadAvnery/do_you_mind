import json

def parse_pose(context, snapshot):
    context.save('translation.json', json.dumps(dict(
        x = snapshot.pose.translation.x,
        y = snapshot.pose.translation.y,
        z = snapshot.pose.translation.z,
    )))
    context.save('rotation.json', json.dumps(dict(
        x = snapshot.pose.rotation.x,
        y = snapshot.pose.rotation.y,
        z = snapshot.pose.rotation.z,
        w = snapshot.pose.rotation.w,
    )))
parse_pose.fields = ['rotation', 'translation']