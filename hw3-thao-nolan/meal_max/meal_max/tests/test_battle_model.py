import logging
import pytest


from meal_max.models.kitchen_model import Meal, update_meal_stats
from meal_max.utils.logger import configure_logger
from meal_max.utils.random_utils import get_random
from meal_max.models.battle_model import BattleModel


@pytest.fixture()
def battle_model():
    """Fixture to provide a new instance of BattleModel for each test."""
    return BattleModel()

# @pytest.fixture 
# def mock_update_

@pytest.fixture
def sample_combatant_1():
    return Meal(1, "testName", "testCuisine", 0.5, "LOW")

@pytest.fixture
def sample_combatant_1():
    return Meal(1, "testName", "testCuisine", 0.5, "LOW")



def test_battle(): 
    """Test battle"""



def test_valid_num_combatants(mock_cursor): 
    """Testing for the valid number of combatants"""



def test_clear_combatants(): 
    """check to see if clear the combatants array"""
    sampleBattle = BattleModel()
    sampleBattle.combatants[0] = sample_combatant_1

    # check that meal has been added to the array
    assert len(sampleBattle.combatants) == 1 

    sampleBattle.clear()
    # check that meal has been cleared
    assert len(sampleBattle.combatants) == 0
    


def test_empty_clear_combatants():{

}  

def test_get_battle_score(mock_cursor): {

}
    
def test_get_combantants(): {

}
    
def test_prep_combatants(mock_cursor): {

}
    

