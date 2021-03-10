class TX:
    def __init__(self):
        self.clds = set()
        self.prts = set()

        self.timestamp = 0
        self.index = 0
        self.depth = 0
        self.trusty = 0
        self.good = 0
        self.bad = 0

        # Validation
        self.status = None   # conflicted / confirmed / deactivated / None
        self.confl_tx = None # conflicted TX with this TX
        self.t_confl = None
        self.t_conf = None
        self.t_deact = None
        self.validators = set()


class DAG:
    def __init__(self):
        pass