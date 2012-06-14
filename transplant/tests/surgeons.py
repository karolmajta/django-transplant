from ..surgeons import NopSurgeon

class FaultySurgeon(NopSurgeon):
    
    def merge(self, receiver, donor):
        raise RuntimeError("Hello faulty surgeon!")
