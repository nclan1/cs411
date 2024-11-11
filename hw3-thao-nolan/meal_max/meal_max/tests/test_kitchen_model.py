from contextlib import contextmanager
import re
import sqlite3

import pytest

from meal_max.models.kitchen_model import (
    Meal,
    create_meal,
    delete_meal,
    get_leaderboard,
    get_meal_by_id,
    get_meal_by_name,
    update_meal_stats,
)
######################################################
#
#    Fixtures
#
######################################################

def normalize_whitespace(sql_query: str) -> str:
    return re.sub(r'\s+', ' ', sql_query).strip()


# Mocking the database connection for tests
@pytest.fixture
def mock_cursor(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()

    # Mock the connection's cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  # Default return for queries
    mock_cursor.fetchall.return_value = []
    mock_cursor.commit.return_value = None

    # Mock the get_db_connection context manager from sql_utils
    @contextmanager
    def mock_get_db_connection():
        yield mock_conn  # Yield the mocked connection object
    mocker.patch("meal_max.models.kitchen_model.get_db_connection", mock_get_db_connection)

    return mock_cursor  # Return the mock cursor so we can set expectations per test

######################################################
#
#    Create and delete Meals
#
######################################################

def test_create_meal(mock_cursor):
    """Test creating a new Meal in the catalog."""
    
    create_meal(meal="Meal Name", cuisine="Cuisine Name", price=6.2, difficulty="LOW")
    
    expected_query = normalize_whitespace("""
                INSERT INTO meals (meal, cuisine, price, difficulty)
                VALUES (?, ?, ?, ?)
            """)
    
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    
    # Assert that the SQL query was correct
    assert actual_query == expected_query, "The SQL query did not match the expected structure."
    
    actual_arguments = mock_cursor.execute.call_args[0][1]
    
    # Assert that the SQL query was executed with the correct arguments
    expected_arguments = ("Meal Name", "Cuisine Name", 6.2, "LOW")
    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}."
    
def test_create_meal_duplicate(mock_cursor):
    
    """Test creating a Meal with a duplicate name, cuisine, price, difficulty (should raise an error)."""

    # Simulate that the database will raise an IntegrityError due to a duplicate entry
    mock_cursor.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed: meal.name, meal.cuisine, meal.price, meal.difficulty")

    # Expect the function to raise a ValueError with a specific message when handling the IntegrityError
    with pytest.raises(ValueError, match="Meal with name 'Meal Name' already exists"):
        create_meal(meal="Meal Name", cuisine="Cuisine Name", price=6.2, difficulty="LOW")

def test_create_meal_invalid_price():
    """Test error when creating a meal with invalid price (negative price)"""
    
    with pytest.raises(ValueError, match="Invalid price: -6.2. Price must be a positive number."):
        create_meal(meal="Meal Name", cuisine="Cuisine Name", price=-6.2, difficulty="LOW")

def test_create_meal_invalid_difficulty():
    """Test error when creating a meal with invalid difficulty """
    with pytest.raises(ValueError, match="Invalid difficulty level: randomDifficulty. Must be 'LOW', 'MED', or 'HIGH'."):
        create_meal(meal="Meal Name", cuisine="Cuisine Name", price=6.2, difficulty="randomDifficulty")


def test_delete_meal(mock_cursor):
    """Test soft deleting a Meal from the catalog by meal_id"""
    
    #meal exists simulation
    mock_cursor.fetchone.return_value = ([False])
    
    delete_meal(1)
    
    # Normalize the sql for select and update
    expected_select_sql = normalize_whitespace("SELECT deleted FROM meals WHERE id = ?")
    expected_update_sql = normalize_whitespace("UPDATE meals SET deleted = TRUE WHERE id = ?")
    
    #both calls to execute and call_args_list
    actual_select_sql = normalize_whitespace(mock_cursor.execute.call_args_list[0][0][0])
    actual_update_sql = normalize_whitespace(mock_cursor.execute.call_args_list[1][0][0])
    
        # Ensure the correct SQL queries were executed
    assert actual_select_sql == expected_select_sql, "The SELECT query did not match the expected structure."
    assert actual_update_sql == expected_update_sql, "The UPDATE query did not match the expected structure."
    
    # Ensure the correct arguments were used in both SQL queries
    expected_select_args = (1,)
    expected_update_args = (1,)

    actual_select_args = mock_cursor.execute.call_args_list[0][0][1]
    actual_update_args = mock_cursor.execute.call_args_list[1][0][1]

    assert actual_select_args == expected_select_args, f"The SELECT query arguments did not match. Expected {expected_select_args}, got {actual_select_args}."
    assert actual_update_args == expected_update_args, f"The UPDATE query arguments did not match. Expected {expected_update_args}, got {actual_update_args}."


def test_delete_meal_bad_id(mock_cursor):
    """Test error when trying to delete a non-existent meal."""
    
    with pytest.raises(ValueError, match="Meal with ID 123 not found"):
        delete_meal(123)
        
def test_delete_meal_already_deleted(mock_cursor):
    """Deleting song that was already deleted."""
    
    mock_cursor.fetchone.return_value = ([True])        
    
    with pytest.raises(ValueError, match="Meal with ID 123 has already been deleted"):
        delete_meal(123)
        
        
#########leader board

def test_get_leaderboard_sorted_by_wins(mock_cursor):
    """Test get_leaderboard sorted by 'wins'."""
    
    # Mock the data returned by the database for leaderboard
    mock_cursor.fetchall.return_value = [
        (1, "Meal A", "Cuisine A", 10.0, "LOW", 10, 8, 0.8),
        (2, "Meal B", "Cuisine B", 12.0, "MED", 15, 7, 0.47),
        (3, "Meal C", "Cuisine C", 8.0, "HIGH", 20, 5, 0.25)
    ]
    
    leaderboard = get_leaderboard(sort_by="wins")
    
    expected_leaderboard = [
        {
            'id': 1,
            'meal': "Meal A",
            'cuisine': "Cuisine A",
            'price': 10.0,
            'difficulty': "LOW",
            'battles': 10,
            'wins': 8,
            'win_pct': 80.0
        },
        {
            'id': 2,
            'meal': "Meal B",
            'cuisine': "Cuisine B",
            'price': 12.0,
            'difficulty': "MED",
            'battles': 15,
            'wins': 7,
            'win_pct': 47.0
        },
        {
            'id': 3,
            'meal': "Meal C",
            'cuisine': "Cuisine C",
            'price': 8.0,
            'difficulty': "HIGH",
            'battles': 20,
            'wins': 5,
            'win_pct': 25.0
        },
    ]
    
    assert leaderboard == expected_leaderboard, f"Expected {expected_leaderboard}, got {leaderboard}"

        
        
######################################################
#
#    Get Meal
#
######################################################

def test_get_meal_by_id(mock_cursor):
    
    #simulate meal exists, the 1 is the id
    mock_cursor.fetchone.return_value = (1, "Meal Name", "Cuisine Name", 6.2, "LOW")
    
    result = get_meal_by_id(1)
    
    expected_result = Meal(1, "Meal Name", "Cuisine Name", 6.2, "LOW")
    
    assert result == expected_result, f"Expected {expected_result}, got {result}"
    
    expected_query = normalize_whitespace("SELECT id, meal, cuisine, price, difficulty, deleted FROM meals WHERE id = ?")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    
    assert actual_query == expected_query, "The SQL query did not match the expected structure."
    
    # Extract the arguments used in the SQL call
    actual_arguments = mock_cursor.execute.call_args[0][1]

    # Assert that the SQL query was executed with the correct arguments
    expected_arguments = (1,)
    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}."

def test_get_meal_by_id_bad_id(mock_cursor):
    
    #no meal exists
    mock_cursor.fetchone.return_value = None
    
    # Expect a valueError meal id not found
    with pytest.raises(ValueError, match="Meal with ID 123 not found"):
        get_meal_by_id(123)
        
def test_get_meal_by_name_bad_name(mock_cursor):
    
    #no meal exists
    mock_cursor.fetchone.return_value = None
    
    # Expect a valueError meal id not found
    with pytest.raises(ValueError, match="Meal with name TestingMeal not found"):
        get_meal_by_name("TestingMeal")
        
        
def test_update_meal_stats(mock_cursor):
    """Test updating the meal stats based on battle results"""
    
    mock_cursor.fetchone.return_value = [False]
    
    meal_id = 1
    battle_result = "win"
    
    update_meal_stats(meal_id, battle_result)
    
    expected_query = normalize_whitespace("""UPDATE meals SET battles = battles + 1, wins = wins + 1 WHERE id = ?""")
    
    actual_query = normalize_whitespace(mock_cursor.execute.call_args_list[1][0][0])
    
    assert actual_query == expected_query, "The SQL query did not match the expected structure."
    
    actual_arguments = mock_cursor.execute.call_args_list[1][0][1]
    
    expected_arguments = (meal_id,)
    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}."
        
        
def test_update_meal_stats_deleted_meal(mock_cursor):
    """Test error when trying to update meal stats for deleted Meal"""
    
    mock_cursor.fetchone.return_value = [True]
    
    with pytest.raises(ValueError, match="Meal with ID 1 has been deleted"):
        update_meal_stats(1, "win")
        
    mock_cursor.execute.assert_called_once_with("SELECT deleted FROM meals WHERE id = ?", (1,))