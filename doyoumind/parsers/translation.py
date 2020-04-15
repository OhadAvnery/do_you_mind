import json

def parse_translation(context, snapshot):
    context.save('translation.json', json.dumps(dict(
        x = snapshot.pose.translation.x,
        y = snapshot.pose.translation.y,
        z = snapshot.pose.translation.z,
    )))
parse_translation.fields = ['translation']