from dataclasses import dataclass, Field 

@dataclass(frozen = True)
class RetryPolicy: 
    max_retries : int = Field(default =  3, ge = 0)
    initial_delay : float = 1.0
    max_delay : float = 30.0


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

