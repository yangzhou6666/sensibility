class Callback: ...

class ModelCheckpoint(Callback):
    def __init__(self, filepath: str, monitor: str='val_loss', verbose: int=0, save_best_only: int=False, save_weights_only: int=False, mode: str='auto', period: int=1) -> None: ...

class CSVLogger(Callback):
    def __init__(self, filename: str, separator: str=',', append: bool=False) -> None: ...

class EarlyStopping(Callback):
    def __init__(self, monitor: str='val_loss', min_delta: float=0, patience: int=0, verbose: int=0, mode: str='auto') -> None: ...
