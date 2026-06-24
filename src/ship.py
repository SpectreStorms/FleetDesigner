from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Dict, Optional, Type


class Classification(Enum):
    """Possible classifications of ships"""
    DESTROYER = auto()
    CRUISER = auto()
    BATTLESHIP = auto()


class Module(ABC):
    """Base class for ship modules which determine ship statistics"""
    _name: str
    _allowed_ships: list[Classification]

    @abstractmethod
    def __init__(self, name: str, allowed_ships: list[Classification]):
        self._name = name
        self._allowed_ships = allowed_ships

    @property
    def name(self)->str:
        return self._name
    
    @property
    def allowed_ships(self)->list[Classification]:
        return self._allowed_ships
    
    def __str__(self)->str:
        return self.name
    
    @abstractmethod
    def __repr__(self)->str:
        return f'Module(name={self.name}, allowed_ships={self.allowed_ships})'


class Armament(Module):
    """Class for modules that fulfill the Armament slots"""
    _damage: int = 0

    def __init__(self, name: str, allowed_ships: list[Classification], damage: int):
        super().__init__(name, allowed_ships)
        self._damage = damage 
    
    @property
    def damage(self)->int:
        return self._damage
    
    def __repr__(self)->str:
        return f'Armament(name={self.name!r}, allowed_ships={self.allowed_ships!r}, damage={self.damage}'


class Engine(Module):
    """Class for modules that fulfill the engine slot"""
    _propulsion: int = 0

    def __init__(self, name: str, allowed_ships: list[Classification], propulsion: int):
        super().__init__(name, allowed_ships)
        self._propulsion = propulsion
    
    @property
    def propulsion(self)->int:
        return self._propulsion
    
    def __repr__(self)->str:
        return f'Engine(name={self.name!r}, allowed_ships={self.allowed_ships!r}, propulsion={self.propulsion})'


class Armor(Module):
    """Class for modules that fulfill the armor slot"""
    _armor: int =  0

    def __init__(self, name: str, allowed_ships: list[Classification], protection: int):
        super().__init__(name, allowed_ships)
        self._protection = protection

    @property
    def protection(self)->int:
        return self._protection
    
    def __repr__(self)->str:
        return f'Armor(name={self.name!r}, allowed_ships={self.allowed_ships!r}, protection={self.protection})'
    

class ModuleSystem(ABC):
    """Base class for ship module systems"""
    _designated_classification: Classification
    _SLOT_CONFIG: Dict[str, Type[Module]]

    @abstractmethod
    def __init__(self, classification: Classification):
        self._designated_classification = classification
        self._equipped_modules: Dict[str, Optional[Module]] = {slot_name: None for slot_name in self.SLOT_CONFIG}

    def equip(self, module: Module, target_slot: str)->bool:
        if self._designated_classification not in module.allowed_ships:
            print("Wrong ship type")
            return False
        if target_slot not in self.SLOT_CONFIG:
            print("Slot not found")
            return False
        if not isinstance(module, self.SLOT_CONFIG[target_slot]):
            print("Wrong equipment type")
            return False

        self._equipped_modules[target_slot] = module
        return True

    @property
    def designated_classification(self)->Classification:
        return self._designated_classification

    @property
    def SLOT_CONFIG(self)->Dict[str, Type[Module]]:
        return self._SLOT_CONFIG

    @property
    def equipped_modules(self)->Dict[str, Optional[Module]]:
        return self._equipped_modules
    
    def __repr__(self)->str:
        return f'ModuleSystem(designated_classification={self.designated_classification}, SLOT_CONFIG={self.SLOT_CONFIG}), equipped_modules={self.equipped_modules}'


class DestroyerModuleSystem(ModuleSystem):
    """Module system for destroyers"""
    _SLOT_CONFIG = {
        "engine": Engine,
        "armor": Armor,
        "armament_one": Armament,
        "armament_two": Armament
    }

    def __init__(self):
        super().__init__(Classification.DESTROYER)

class CruiserModuleSystem(ModuleSystem):
    """Module system for cruisers"""
    _SLOT_CONFIG = {
        "engine": Engine,
        "armor": Armor,
        "armament_one": Armament,
        "armament_two": Armament,
        "armament_three": Armament
    }

    def __init__(self):
        super().__init__(Classification.CRUISER)

class BattleshipModuleSystem(ModuleSystem):
    """Module system for battleships"""
    _SLOT_CONFIG = {
        "engine": Engine,
        "armor": Armor,
        "armament_one": Armament,
        "armament_two": Armament,
        "armament_three": Armament,
        "armament_four": Armament
    }

    def __init__(self):
        super().__init__(Classification.BATTLESHIP)

class Ship:
    """The core unit of the fleet; stats are determined by the modules"""
    _name: str
    _classification: Classification
    _modules: ModuleSystem
    
    _health: int = 0
    _armor: int = 0
    _attack: int = 0

    def __init__(self, name: str, classification: Classification):
        self._name = name
        self._classification = classification
        if classification is Classification.DESTROYER:
            self._modules = DestroyerModuleSystem()
        elif classification is Classification.CRUISER:
            self._modules = CruiserModuleSystem()
        elif classification is Classification.BATTLESHIP:
            self._modules = BattleshipModuleSystem()


    def equip(self, module: Module, target_slot: str):
        self.modules.equip(module, target_slot)

        for slot in self.modules.equipped_modules.values():
            if not slot:
                continue
            
            if isinstance(slot, Engine):
                pass
            elif isinstance(slot, Armament):
                self._attack += slot.damage
            elif isinstance(slot, Armor):
                self._armor += slot.protection
        

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
    def modules(self)->ModuleSystem:
        return self._modules
    
    def __str__(self)->str:
        return self.name
    
    def __repr__(self)->str:
        return f'Ship(name={self.name!r}, classification={self.classification}, health={self.health}, armor={self.armor}, modules={self.modules})'
