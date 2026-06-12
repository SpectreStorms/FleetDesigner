import pytest
from src.ship import Ship, Module, Classification

@pytest.fixture
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
    ship = request.getfixturevalue(ship_fixture)

    assert ship.name == exp_name
    assert ship.classification == exp_classification
    assert ship.armor == exp_armor
    assert ship.attack == exp_attack
    assert ship.health == exp_health

@pytest.mark.parametrize("ship_fixture, repr", [
    ("ship_one", "Ship(name='Test', classification=Classification.DESTROYER, health=0, armor=0, modules={})"),
    ("ship_two", "Ship(name='', classification=Classification.CRUISER, health=0, armor=0, modules={})"),
    ("ship_three", "Ship(name='New Ship', classification=Classification.BATTLESHIP, health=0, armor=0, modules={})")
])

def test_ship_repr(request, ship_fixture: str, repr: str):
    """Test __repr__ method of the Ship class"""
    ship = request.getfixturevalue(ship_fixture)

    assert ship.__repr__() == repr
