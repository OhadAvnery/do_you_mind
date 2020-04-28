import json

def parse_pose(context, snapshot):
    snap_dict = json.loads(snapshot)

    translation_dict = snap_dict['pose']['translation']
    context.save('translation.json', json.dumps(translation_dict))

    rotation_dict = snap_dict['pose']['rotation']
    context.save('rotation.json', json.dumps(rotation_dict))

parse_pose.fields = ['rotation', 'translation']