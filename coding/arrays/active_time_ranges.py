"""Active Time Ranges starter file."""

class ActiveTimeRanges:
    def __init__(self, intervals: list[list[int]]):
        self.intervals, self.total_active_time = self.merge_and_measure(intervals)

    def merge_and_measure(self, intervals: list[list[int]]) -> tuple[list[list[int]], int]:
        intervals = sorted(intervals, key=lambda x: x[0])
        new_intervals = []
        counter=0
        for start, end in intervals:
            if not new_intervals:
                new_intervals.append([start, end])
            elif new_intervals[-1][1] >= start and new_intervals[-1][1] < end:
                new_intervals[-1][1] = end
            elif end <= new_intervals[-1][1] and start >= new_intervals[-1][0]:
                continue
            elif end != new_intervals[-1][1] and start != new_intervals[-1][0]:
                counter=counter+(new_intervals[-1][1]-new_intervals[-1][0])
                new_intervals.append([start, end])
        counter=counter+(new_intervals[-1][1]-new_intervals[-1][0])
        print(new_intervals, counter)
        return tuple(new_intervals), counter 

if __name__ == "__main__":
    atr = ActiveTimeRanges([[1, 3], [2, 6], [8, 10], [15, 18]])
    print( atr.intervals == tuple([[1, 6], [8, 10], [15, 18]]) and atr.total_active_time ==  10)
    atr = ActiveTimeRanges([[1, 4], [4, 5]])
    print( atr.intervals == tuple([[1, 5]]) and atr.total_active_time ==  4)
    atr = ActiveTimeRanges([[7, 9], [1, 2], [2, 4], [10, 12]])
    print( atr.intervals == tuple([[1, 4], [7, 9], [10, 12]]) and atr.total_active_time ==  7)
