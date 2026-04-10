# DO NOT COPY - FAILED Program due to 'key' concept around the need to capture every log

# This example is wrong. For log sampling you need every log, their is no need for uniqueness. 
# Instead, what should happen is capture everyting in a given time window. Within the window 
# you should search for the key. 



from functools import lru_cache

class Logger:
    _LogLevel = ('DEBUG', 'INFO', 'WARN', 'ERROR')
    _ttl = 60
    _cache = {}
    _sampling_limits_count = {}

    def __init__(self, level: str = "INFO", sampling_limits=None, sampling_limits_count=None):
        self.level = level
        self.sampling_limits = sampling_limits or {}
        self.sampling_limits_count = sampling_limits or {}

    @classmethod
    def rateLimiter(cls, message_key : str, message : str, timestamp_sec : int, threshold : int, message_key_count : int):
        key_val = (message_key, message)
        counter=0

        for (loop_message_key, loop_message), creation_time in cls._cache.items():
            print(f"loop_message_key:{loop_message_key}, loop_message={loop_message}")
            if loop_message_key == message_key and loop_message == message and creation_time == timestamp_sec:
                print("ERROR: Duplicate Entry ->", loop_message_key, loop_message, timestamp_sec)
                return message_key_count, False
            elif message_key == loop_message_key and creation_time >= timestamp_sec-cls._ttl:
                counter = counter+1
                print(f"counter:{counter}")
            elif creation_time < timestamp_sec-cls._ttl:
                del cls._cache[(loop_message_key, loop_message)]
        if counter >= threshold:
            print(f"ERROR: Blocking due to too many connections:", key_val, ", timestamp:",timestamp_sec, ", max message count:", threshold)
            return counter, False
        else:
            print(f"INFO: Adding connection:{key_val}, timestamp:{timestamp_sec}, max message count:{threshold}, current:{counter}")
            cls._cache[key_val] = timestamp_sec
            print(f"Cache Entry for Timestamp:{cls._cache.get(key_val)}")
            return counter+1, True

    @classmethod
    @lru_cache(maxsize=5)
    def get_log_escalate(cls, current_level: str, level : str ) -> bool:
        # Return True if current_level is at or above the required level
        return cls._LogLevel.index(current_level) >= cls._LogLevel.index(level)
        
    @lru_cache(maxsize=50)
    def get_sampling_limits(self, message_key: str):
        return int(self.sampling_limits.get(message_key, 1))  # 1 is a default threshold
    
    def get_sampling_limits_count(self, message_key: str):
        return int(self.sampling_limits_count.get(message_key, 0))  # 1 is a default threshold

    def log(self, level: str, message_key: str, message: str, timestamp_sec: int) -> bool:
        if self.get_log_escalate(level, self.level):
            threshold = self.get_sampling_limits(message_key)
            current_count=self.get_sampling_limits_count(message_key)
            new_count, bool_success = self.rateLimiter(message_key, message, timestamp_sec, threshold, current_count)
            if bool_success:
                print(f"INFO: {bool_success} -> connection new:{new_count} old:{current_count}, level:{level} message_key:{message_key} message:{message} threshold:{threshold} " ) 
                self.sampling_limits_count[message_key] = new_count
                return True
            else:
                print(f"ERROR: {bool_success} -> connection new:{new_count} old:{current_count}, level:{level} message_key:{message_key} message:{message} threshold:{threshold} " ) 
                return False
            
        print(f"INFO: No need to add since this the Log Level({level}) is below the Log Level required({self.level}) to pass downstream.")
        return False
        


if __name__ == "__main__":
    logger = Logger(sampling_limits={
        'k1': 2,  # Only 2 ERROR logs allowed for k1
        'k2': 1,  # Only 1 ERROR log allowed for k2
        'k3': 3,  # Only 3 ERROR logs allowed for k3
        'k4': 2,  # Only 2 ERROR logs allowed for k4
        'k5': 1,  # Only 1 ERROR log allowed for k5
        'k6': 2,  # Only 2 ERROR logs allowed for k6
        'k7': 1,  # Only 1 ERROR log allowed for k7
        'k8': 2,  # Only 2 ERROR logs allowed for k8
        'k9': 1,  # Only 1 ERROR log allowed for k9
        'k10': 2, # Only 2 ERROR logs allowed for k10
        'k11': 1, # Only 1 ERROR log allowed for k11
        'k12': 2, # Only 2 ERROR logs allowed for k12
        'k13': 1  # Only 1 ERROR log allowed for k13
    })
    assert logger.log("INFO", 'k', 'x', 0 ) == True, "Failed: INFO k x 0 should be True - INFO is emitted by default"
    assert logger.log("ERROR", 'k1', 'x', 0 ) == True, "Failed: ERROR k1 x 0 should be True - first ERROR for k1, limit is 2"
    assert logger.log("ERROR", 'k1', 'x', 0 ) == False, "Failed: ERROR k1 x 0 should be False - duplicate timestamp, blocked"
    assert logger.log("DEBUG", 'k2', 'y', 1 ) == False, "Failed: DEBUG k2 y 1 should be False - DEBUG below INFO"
    assert logger.log("INFO", 'k2', 'y', 2 ) == True, "Failed: INFO k2 y 2 should be True - first and only allowed for k2"
    assert logger.log("WARN", 'k2', 'y', 3 ) == False, "Failed: WARN k2 y 3 should be False - over limit for k2"
    assert logger.log("ERROR", 'k2', 'y', 4 ) == False, "Failed: ERROR k2 y 4 should be False - over limit for k2"
    assert logger.log("ERROR", 'k2', 'y', 4 ) == False, "Failed: ERROR k2 y 4 should be False - duplicate timestamp, blocked"
    assert logger.log("INFO", 'k3', 'z', 5 ) == True, "Failed: INFO k3 z 5 should be True - INFO is emitted by default"
    assert logger.log("ERROR", 'k3', 'z', 6 ) == True, "Failed: ERROR k3 z 6 should be True - first ERROR for k3, limit is 3"
    assert logger.log("ERROR", 'k3', 'z', 7 ) == True, "Failed: ERROR k3 z 7 should be True - second ERROR for k3, limit is 3"
    assert logger.log("ERROR", 'k3', 'z', 8 ) == True, "Failed: ERROR k3 z 8 should be True - third ERROR for k3, limit is 3"
    assert logger.log("ERROR", 'k3', 'z', 9 ) == False, "Failed: ERROR k3 z 9 should be False - over limit for k3"
    assert logger.log("DEBUG", 'k4', 'a', 10 ) == False, "Failed: DEBUG k4 a 10 should be False - DEBUG below INFO"
    assert logger.log("INFO", 'k4', 'a', 11 ) == True, "Failed: INFO k4 a 11 should be True - INFO is emitted by default"
    assert logger.log("WARN", 'k4', 'a', 12 ) == True, "Failed: WARN k4 a 12 should be True - WARN is emitted by default"
    assert logger.log("ERROR", 'k4', 'a', 13 ) == True, "Failed: ERROR k4 a 13 should be True - first ERROR for k4, limit is 2"
    assert logger.log("ERROR", 'k4', 'a', 14 ) == True, "Failed: ERROR k4 a 14 should be True - second ERROR for k4, limit is 2"
    assert logger.log("ERROR", 'k4', 'a', 15 ) == False, "Failed: ERROR k4 a 15 should be False - over limit for k4"
    assert logger.log("INFO", 'k5', 'b', 16 ) == True, "Failed: INFO k5 b 16 should be True - INFO is emitted by default"
    assert logger.log("ERROR", 'k5', 'b', 17 ) == True, "Failed: ERROR k5 b 17 should be True - first ERROR for k5, limit is 1"
    assert logger.log("ERROR", 'k5', 'b', 18 ) == False, "Failed: ERROR k5 b 18 should be False - over limit for k5"
    assert logger.log("DEBUG", 'k6', 'c', 19 ) == False, "Failed: DEBUG k6 c 19 should be False - DEBUG below INFO"
    assert logger.log("INFO", 'k6', 'c', 20 ) == True, "Failed: INFO k6 c 20 should be True - INFO is emitted by default"
    assert logger.log("WARN", 'k6', 'c', 21 ) == True, "Failed: WARN k6 c 21 should be True - WARN is emitted by default"
    assert logger.log("ERROR", 'k6', 'c', 22 ) == True, "Failed: ERROR k6 c 22 should be True - first ERROR for k6, limit is 2"
    assert logger.log("ERROR", 'k6', 'c', 23 ) == True, "Failed: ERROR k6 c 23 should be True - second ERROR for k6, limit is 2"
    assert logger.log("ERROR", 'k6', 'c', 24 ) == False, "Failed: ERROR k6 c 24 should be False - over limit for k6"
    assert logger.log("INFO", 'k7', 'd', 25 ) == True, "Failed: INFO k7 d 25 should be True - INFO is emitted by default"
    assert logger.log("ERROR", 'k7', 'd', 26 ) == True, "Failed: ERROR k7 d 26 should be True - first ERROR for k7, limit is 1"
    assert logger.log("ERROR", 'k7', 'd', 27 ) == False, "Failed: ERROR k7 d 27 should be False - over limit for k7"
    assert logger.log("DEBUG", 'k8', 'e', 28 ) == False, "Failed: DEBUG k8 e 28 should be False - DEBUG below INFO"
    assert logger.log("INFO", 'k8', 'e', 29 ) == True, "Failed: INFO k8 e 29 should be True - INFO is emitted by default"
    assert logger.log("WARN", 'k8', 'e', 30 ) == True, "Failed: WARN k8 e 30 should be True - WARN is emitted by default"
    assert logger.log("ERROR", 'k8', 'e', 31 ) == True, "Failed: ERROR k8 e 31 should be True - first ERROR for k8, limit is 2"
    assert logger.log("ERROR", 'k8', 'e', 32 ) == True, "Failed: ERROR k8 e 32 should be True - second ERROR for k8, limit is 2"
    assert logger.log("ERROR", 'k8', 'e', 33 ) == False, "Failed: ERROR k8 e 33 should be False - over limit for k8"
    assert logger.log("INFO", 'k9', 'f', 34 ) == True, "Failed: INFO k9 f 34 should be True - INFO is emitted by default"
    assert logger.log("ERROR", 'k9', 'f', 35 ) == True, "Failed: ERROR k9 f 35 should be True - first ERROR for k9, limit is 1"
    assert logger.log("ERROR", 'k9', 'f', 36 ) == False, "Failed: ERROR k9 f 36 should be False - over limit for k9"
    assert logger.log("DEBUG", 'k10', 'g', 37 ) == False, "Failed: DEBUG k10 g 37 should be False - DEBUG below INFO"
    assert logger.log("INFO", 'k10', 'g', 38 ) == True, "Failed: INFO k10 g 38 should be True - INFO is emitted by default"
    assert logger.log("WARN", 'k10', 'g', 39 ) == True, "Failed: WARN k10 g 39 should be True - WARN is emitted by default"
    assert logger.log("ERROR", 'k10', 'g', 40 ) == True, "Failed: ERROR k10 g 40 should be True - first ERROR for k10, limit is 2"
    assert logger.log("ERROR", 'k10', 'g', 41 ) == True, "Failed: ERROR k10 g 41 should be True - second ERROR for k10, limit is 2"
    assert logger.log("ERROR", 'k10', 'g', 42 ) == False, "Failed: ERROR k10 g 42 should be False - over limit for k10"
    assert logger.log("INFO", 'k11', 'h', 43 ) == True, "Failed: INFO k11 h 43 should be True - INFO is emitted by default"
    assert logger.log("ERROR", 'k11', 'h', 44 ) == True, "Failed: ERROR k11 h 44 should be True - first ERROR for k11, limit is 1"
    assert logger.log("ERROR", 'k11', 'h', 45 ) == False, "Failed: ERROR k11 h 45 should be False - over limit for k11"
    assert logger.log("DEBUG", 'k12', 'i', 46 ) == False, "Failed: DEBUG k12 i 46 should be False - DEBUG below INFO"
    assert logger.log("INFO", 'k12', 'i', 47 ) == True, "Failed: INFO k12 i 47 should be True - INFO is emitted by default"
    assert logger.log("WARN", 'k12', 'i', 48 ) == True, "Failed: WARN k12 i 48 should be True - WARN is emitted by default"
    assert logger.log("ERROR", 'k12', 'i', 49 ) == True, "Failed: ERROR k12 i 49 should be True - first ERROR for k12, limit is 2"
    assert logger.log("ERROR", 'k12', 'i', 50 ) == True, "Failed: ERROR k12 i 50 should be True - second ERROR for k12, limit is 2"
    assert logger.log("ERROR", 'k12', 'i', 51 ) == False, "Failed: ERROR k12 i 51 should be False - over limit for k12"
    assert logger.log("INFO", 'k13', 'j', 52 ) == True, "Failed: INFO k13 j 52 should be True - INFO is emitted by default"
    assert logger.log("ERROR", 'k13', 'j', 53 ) == True, "Failed: ERROR k13 j 53 should be True - first ERROR for k13, limit is 1"
    assert logger.log("ERROR", 'k13', 'j', 54 ) == False, "Failed: ERROR k13 j 54 should be False - over limit for k13"



""" 
Build test with inputs to validate expected input and output
    { level: "INFO", message_key: 'k', message: 'x', timestamp_sec: 0 }
"""