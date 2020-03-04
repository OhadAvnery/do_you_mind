import struct
import datetime
import time

class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        rep = f'Thought(user_id={self.user_id}, timestamp={repr(self.timestamp)}, thought="{self.thought}")'
        return rep

    def __str__(self):
        time_date_format = time.strftime("%Y-%m-%d %H:%M:%S", self.timestamp.timetuple())
        return f'[{time_date_format}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        if not isinstance(other, Thought):
            return False
        return self.user_id==other.user_id and self.timestamp==other.timestamp \
            and self.thought==other.thought

    def serialize(self):
        n = len(self.thought)
        user_id_bytes = struct.pack("Q", self.user_id)
        timestamp_epoch = struct.pack("Q", int(self.timestamp.timestamp()))
        thought_size = struct.pack("I", n)
        thought_data = struct.pack("{:d}s".format(n), str.encode(self.thought))
        binary_data = user_id_bytes + timestamp_epoch + thought_size + thought_data
        return binary_data

    #class method
    def deserialize(data):
        offset = 0

        user_id = struct.unpack_from("Q", data, offset)[0]
        offset += struct.calcsize("Q")

        timestamp_epoch = struct.unpack_from("Q", data, offset)[0]
        timestamp_datetime = datetime.datetime.fromtimestamp(timestamp_epoch)
        offset += struct.calcsize("Q")

        #we're skipping this because we can calculate the thought size ourselves.
        thought_size = struct.unpack_from("I", data, offset)[0]
        offset += struct.calcsize("I")

        thought_data = struct.unpack_from("{:d}s".format(thought_size), \
                                         data, offset)[0].decode()

        return Thought(user_id, timestamp_datetime, thought_data)

            



#time_date_format = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(timestamp))