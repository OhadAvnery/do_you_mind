import json

def parse_feelings(context, snapshot):
    context.save('feelings.json', json.dumps(dict(
        hunger = snapshot.feelings.hunger,
        thirst = snapshot.feelings.thirst,
        exhaustion = snapshot.feelings.exhaustion,
        happiness = snapshot.feelings.happiness,
    )))
parse_feelings.field = 'feelings'