import logging
import pytest


from meal_max.models.kitchen_model import Meal, update_meal_stats
from meal_max.utils.logger import configure_logger
from meal_max.utils.random_utils import get_random
from meal_max.models.battle_model import BattleModel

def battle_model():
    """Fixture to provide a new instance of BattleModel for each test."""
    return BattleModel()

@pytest.fixture
def sample_meal_1():
    return Meal(1, "Meal 1", "testCuisine", 0.5, "LOW")

@pytest.fixture
def sample_meal_2():
    return Meal(2, "Meal 2", "testCuisine", 0.7, "MED")

@pytest.fixture
def sample_battle(sample_meal_1, sample_meal_2):
    return [sample_meal_1, sample_meal_2]


def test_battle(battle_model, sample_battle): 
    """Test that there are two combatants in the battle"""
    battle_model.combatants.extend(sample_battle)
    assert len(battle_model.combatants) == 2
    assert battle_model.combatants[0].meal == "Meal 1"
    assert battle_model.combatants[1].meal == "Meal 2"

def test_valid_num_combatants(sample_battle): 
    """Testing for the valid number of combatants"""
    assert len(sample_battle) == 2

def test_clear_combatants(sample_battle): 
    """Check to see if clear the combatants array"""
    sample_battle = BattleModel()
    sample_battle.combatants[0] = sample_meal_1

    # check that meal has been added to the array
    assert len(sample_battle.combatants) == 1

    sample_battle.clear_combatants()
    # check that meal has been cleared
    assert len(sample_battle.combatants) == 0, "Combatants should be empty after clearing"
    

def test_empty_clear_combatants(battle_model, caplog):
    """Test clearing combatants when it is empty"""
    battle_model.clear_combatants() 
    assert len(battle_model.combatants) == 0, "Combatants should be empty after clearing"
    assert "Clearing empty combatants" in caplog.text, "Expected warning message when clearing an empty playlist"
    

def test_get_battle_score(battle_model, sample_battle): 
    """Test getting the battle score"""
    expected_score = 1
    battle_model.combatants.extend(sample_battle)
    calculated_score = battle_model.get_battle_score(sample_meal_1)
    assert calculated_score == expected_score, "Scores should be equivalent."

    
def test_get_combantants(battle_model, sample_battle): 
    """Test retrieve the combatants from battle"""
    battle_model.combatants.extend(sample_battle)
    num_combatants = battle_model.get_combatants()
    assert len(battle_model.get_combatants()) == 2, "Number of combatants in a battle is 2"

    
def test_prep_combatants(battle_model, sample_meal_1): 
    """ Test adding combatant to the combatants list"""
    battle_model.prep_combatants(sample_meal_1)
    assert len(battle_model.combatants) == 1
    assert battle_model.combatants[0].meal == 'Meal 1'


