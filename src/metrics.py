class Metrics:
    def __init__(self):
        self.total_requests = 0
        self.cache_hits = 0
        self.semantic_hits = 0
        self.repairs = 0
        self.valid_first_try = 0
        self.total_response_length = 0

    def report(self):
        if self.total_requests == 0:
            return "No evaluation data yet."

        return {
            "Total Requests": self.total_requests,
            "Cache Hit Rate": self.cache_hits / self.total_requests,
            "Semantic Hit Rate": self.semantic_hits / self.total_requests,
            "Repair Rate": self.repairs / self.total_requests,
            "Validation First Try Rate": self.valid_first_try / self.total_requests,
            "Avg Response Length": self.total_response_length / self.total_requests
        }
