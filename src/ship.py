from abc import ABC, abstractmethod
from enum import Enum, auto


class Classification(Enum):
    """Possible classifications of ships"""
    DESTROYER = auto()
    CRUISER = auto()
    BATTLESHIP = auto()


class Ship:
    """The core unit of the fleet; stats are determined by the modules"""
    _name: str
    _classification: Classification
    _modules: dict[Module, int] = {}    # value represents quantity as some modules can have multiple equipped
    
    _health: int = 0
    _armor: int = 0
    _attack: int = 0

    def __init__(self, name: str, classification: Classification):
        self._name = name
        self._classification = classification

    @property
    def name(self)->str:
        return self._name
    
    @property
    def classification(self)->Classification:
        return self._classification

    @property
    def health(self)->int:
        return self._health
    
    @property
    def armor(self)->int:
        return self._armor
    
    @property
    def attack(self)->int:
        return self._attack
    
    @property
    def modules(self)->dict[Module, int]:
        return self._modules
    
    def __str__(self)->str:
        return self.name
    
    def __repr__(self)->str:
        return f'Ship(name={self.name!r}, classification={self.classification}, health={self.health}, armor={self.armor}, modules={self.modules})'


class Module(ABC):
    """Base class for ship modules which determine ship statistics"""
    _name: str
    _type: str

    @abstractmethod
    def __init__(self, name: str, type: str):
        self._name = name
        self._type = type

    @property
    def name(self)->str:
        return self._name
    
    @property
    def type(self)->str:
        return self._type
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'name={self.name}, type={self.type}'
