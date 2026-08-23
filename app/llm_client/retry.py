from dataclasses import dataclass, field 

@dataclass(frozen = True)
class RetryPolicy: 
    max_retries : int = field(default =  3)
    initial_delay : float = 1.0
    max_delay : float = 30.0

    def __post_init__(self):
        if self.max_retries < 0: 
            raise ValueError("max_retries must be non-negative")


import time

class RetryHandler: 
    def __init__(self,policy : RetryPolicy): 
        self.policy = policy

    def execute(self, operation): 
        for attempt in range(self.policy.max_retries + 1): 
            try:
                return operation()
            except Exception: 
                if attempt == self.policy.max_retries: 
                    raise
                else: 
                    delay = min(self.policy.initial_delay * (2 ** attempt), self.policy.max_delay)
                    time.sleep(delay)

