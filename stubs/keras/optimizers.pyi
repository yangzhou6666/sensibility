class Optimizer: ...

class RMSprop(Optimizer):
    def __init__(self, lr: float=0.001, rho: float=0.9, epsilon: float=1e-8, decay: float=0., clipnorm: float=None) -> None: ...
class Adam(Optimizer):
    def __init__(self, lr: float=0.001,  beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0) -> None: ...
class Nadam(Optimizer):
    def __init__(self, lr: float=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, schedule_decay=0.004) -> None: ...
