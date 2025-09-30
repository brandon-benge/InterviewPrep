from collections import defaultdict, deque
from functools import lru_cache

class Logger:
    _LogLevel = ('DEBUG', 'INFO', 'WARN', 'ERROR')
    _ttl = 60
    _hist = defaultdict(deque)

    def __init__(self, level: str = "INFO", sampling_limits=None):
        self.level = level
        self.level_index = Logger._LogLevel.index(level)
        self.sampling_limits = sampling_limits or {}

    @classmethod
    def rateLimiter(cls, message_key : str, timestamp_sec : int, threshold : int ) -> bool:
        dq = cls._hist[message_key]
        # Evict old timestamps for this key
        cutoff = timestamp_sec - cls._ttl + 1
        while dq and dq[0] < cutoff:
            dq.popleft()
        # Decide
        if len(dq) < threshold:
            dq.append(timestamp_sec)
            return True
        return False


    @classmethod
    @lru_cache(maxsize=5)
    def get_log_escalate(cls, current_level: str, level_index : int ) -> bool:
        # Return True if current_level is at or above the required level
        return cls._LogLevel.index(current_level) >= level_index
        
    def get_sampling_limits(self, message_key: str):
        return int(self.sampling_limits.get(message_key, 1))  # 1 is a default threshold

    def log(self, level: str, message_key: str, message: str, timestamp_sec: int) -> bool:
        if self.get_log_escalate(level, self.level_index):
            threshold = self.get_sampling_limits(message_key)
            return self.rateLimiter(message_key, timestamp_sec, threshold)
        return False
        


if __name__ == "__main__":
    # 10 assert tests for the new Logger program
    logger = Logger(sampling_limits={
        'alpha': 2,
        'beta': 1,
        'gamma': 3
    })
    # INFO, threshold not exceeded
    assert logger.log("INFO", 'alpha', 'msg1', 0) == True, "Failed: INFO alpha msg1 0 should be True (first allowed)"
    assert logger.log("INFO", 'alpha', 'msg2', 1) == True, "Failed: INFO alpha msg2 1 should be True (second allowed)"
    assert logger.log("INFO", 'alpha', 'msg3', 2) == False, "Failed: INFO alpha msg3 2 should be False (over limit)"
    # ERROR, threshold not exceeded
    assert logger.log("ERROR", 'beta', 'err1', 3) == True, "Failed: ERROR beta err1 3 should be True (first allowed)"
    assert logger.log("ERROR", 'beta', 'err2', 4) == False, "Failed: ERROR beta err2 4 should be False (over limit)"
    # WARN, threshold not exceeded
    assert logger.log("WARN", 'gamma', 'warn1', 5) == True, "Failed: WARN gamma warn1 5 should be True (first allowed)"
    assert logger.log("WARN", 'gamma', 'warn2', 6) == True, "Failed: WARN gamma warn2 6 should be True (second allowed)"
    assert logger.log("WARN", 'gamma', 'warn3', 7) == True, "Failed: WARN gamma warn3 7 should be True (third allowed)"
    assert logger.log("WARN", 'gamma', 'warn4', 8) == False, "Failed: WARN gamma warn4 8 should be False (over limit)"
    # DEBUG, below INFO
    assert logger.log("DEBUG", 'alpha', 'debug1', 9) == False, "Failed: DEBUG alpha debug1 9 should be False (below INFO)"
    logger = Logger(sampling_limits={
        'k1': 2,  # Only 2 ERROR logs allowed for k1
        'k2': 1,  # Only 1 ERROR log allowed for k2
        'k3': 3,  # Only 3 ERROR logs allowed for k3
        'k4': 2,  # Only 2 ERROR logs allowed for k4
    })