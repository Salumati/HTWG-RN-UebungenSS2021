import heapq


class _EventQueue:
    def __init__(self):
        self.history = []
        self.queue = []
        heapq.heapify(self.queue)

    def pop(self):
        return heapq.heappop(self.queue)

    def push(self, event):
        heapq.heappush(self.queue, event)

    def work(self):
        while self.queue:
            ev = self.pop()
            self.history.append(ev)
            ev.execute()

    def isNotEmpty(self):
        return len(self.queue) > 0

    def __str__(self):
        res = ""
        for ev in self.history:
            res += str(ev) + "\n"

        return res

EventQueue = _EventQueue()