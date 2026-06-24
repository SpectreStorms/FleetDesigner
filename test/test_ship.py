import pytest
from src.ship import Ship, Module, Classification, Engine, Armament, Armor
from typing import Type

@pytest.fixture()
def ship_one()->Ship:
    return Ship("Test", Classification.DESTROYER) 

@pytest.fixture
def ship_two()->Ship:
    return Ship("", Classification.CRUISER)

@pytest.fixture
def ship_three()->Ship:
    return Ship("New Ship", Classification.BATTLESHIP)

@pytest.mark.parametrize("ship_fixture, exp_name, exp_classification, exp_armor, exp_attack, exp_health", [
    ("ship_one", "Test", Classification.DESTROYER, 0, 0, 0),
    ("ship_two", "", Classification.CRUISER, 0, 0, 0),
    ("ship_three", "New Ship", Classification.BATTLESHIP, 0, 0, 0)
])

def test_ship_instantiation(request, ship_fixture: str, exp_name: str, exp_classification: Classification, exp_armor: int, exp_attack: int, exp_health: int):
    """Test correct instantiation of Ship class and attributes"""
    ship: Ship = request.getfixturevalue(ship_fixture)

    assert ship.name == exp_name
    assert ship.classification == exp_classification
    assert ship.armor == exp_armor
    assert ship.attack == exp_attack
    assert ship.health == exp_health

@pytest.mark.parametrize("ship_fixture, exp_parts", [
    ("ship_one", ["name='Test'", "classification=Classification.DESTROYER", "health=0", "armor=0", "modules=ModuleSystem"]),
    ("ship_two", ["name=''", "classification=Classification.CRUISER", "health=0", "armor=0", "modules=ModuleSystem"]),
    ("ship_three", ["name='New Ship'", "classification=Classification.BATTLESHIP", "health=0", "armor=0", "modules=ModuleSystem"])
])

def test_ship_repr(request, ship_fixture: str, exp_parts: list[str]):
    """Test key elements of the Ship class __repr__ method"""
    ship: Ship = request.getfixturevalue(ship_fixture)

    for part in exp_parts:
        assert part in ship.__repr__()

@pytest.fixture
def module_one()->Engine:
    return Engine("Test Engine", [Classification.DESTROYER], 10)

@pytest.fixture
def module_two()->Armor:
    return Armor("Test Armor", [Classification.DESTROYER, Classification.CRUISER], 20)

@pytest.fixture
def module_three()->Armament:
    return Armament("Test Weapon", [Classification.DESTROYER, Classification.BATTLESHIP], 15)

@pytest.mark.parametrize("module_fixture, exp_name, exp_ships_list, exp_stats", [
    ("module_one", "Test Engine", [Classification.DESTROYER], 10),
    ("module_two", "Test Armor", [Classification.DESTROYER, Classification.CRUISER], 20),
    ("module_three", "Test Weapon", [Classification.DESTROYER, Classification.BATTLESHIP], 15)
])

def test_module_instantiation(request, module_fixture: str, exp_name: str, exp_ships_list: list[Classification], exp_stats: int):
    module: Module = request.getfixturevalue(module_fixture)
    assert isinstance(module, Module)

    assert module.name == exp_name
    assert module.allowed_ships == exp_ships_list
    if isinstance(module, Engine):
        assert module.propulsion == exp_stats
    elif isinstance(module, Armament):
        assert module.damage == exp_stats
    elif isinstance(module, Armor):
        assert module.protection == exp_stats

@pytest.mark.parametrize("ship_fixture, module_fixture, target_slot, exp_stats", [
    ("ship_one", "module_one", "engine", [0, 0, 0]),    # Equip engine
    ("ship_one", "module_three", "armament_one", [0, 0, 15]),   # Equip armament
    ("ship_two", "module_two", "armor", [0, 20, 0]),    # Equip armor
    ("ship_two", "module_two", "armament_one", [0, 0, 0]),    # Equip in wrong slot
    ("ship_three", "module_two", "armor", [0, 0, 0]),    # Wrong ship type
    ("ship_one", "module_one", "none", [0,0,0])    # Slot does not exist
])

def test_equip_method(request, ship_fixture: str, module_fixture: str, target_slot: str, exp_stats: list[int]):
    ship: Ship = request.getfixturevalue(ship_fixture)
    module: Module =  request.getfixturevalue(module_fixture)
    ship.equip(module, target_slot)
    assert exp_stats[0] == ship.health
    assert exp_stats[1] == ship.armor
    assert exp_stats[2] == ship.attack
