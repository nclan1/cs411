#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5001/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done


# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
}

# Function to create a meal and add to database

create_meal() {
  meal=$1
  cuisine=$2
  price=$3
  difficulty=$4

  echo "Creating a meal ($meal - $cuisine - $difficulty) to the database..."
  response=$(curl -s -X POST "$BASE_URL/create-meal" -H "Content-Type: application/json" \
    -d "{\"meal\":\"$meal\", \"cuisine\":\"$cuisine\", \"price\":$price, \"difficulty\":\"$difficulty\"}")

  if echo "$response" | grep -q '"status": "combatant added"'; then
    echo "Meal added successfully to database."
  else
    echo "Failed to add meal."
    exit 1
  fi
}

# Function to delete a meal from database

delete_meal() {
  meal_id=$1

  echo "Deleting a meal by ID ($meal_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-meal/$meal_id")
  if echo "$response" | grep -q '"status": "meal deleted"'; then
    echo "Meal deleted successfully by ID ($meal_id)."
  else
    echo "Failed to delete meal by ID ($meal_id)."
    exit 1
  fi
}

# Function to get meal by id

get_meal_by_id() {
  meal_id=$1

  echo "Getting meal by ID ($meal_id)..."

  response=$(curl -s -X GET "$BASE_URL/get-meal-by-id/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by ID ($meal_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Mea JSON (ID $meal_id):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal id ($meal_id)."
    exit 1
  fi
}

# Function to get meal by name

get_meal_by_name() {
  meal_name=$1

  echo "Getting meal by ID ($meal_name)..."

  response=$(curl -s -X GET "$BASE_URL/get-meal-by-name/$meal_name")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by ID ($meal_name)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Mea JSON (ID $meal_name):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal id ($meal_name)."
    exit 1
  fi
}




# Function to initiate battle between combatants

battle() {
  echo "Initiating Battle..."
  response=$(curl -s -X GET "$BASE_URL/battle")

  if echo "$response" | grep -q '"status": "battle complete"'; then
    echo "Battle complete"
    if [ "$ECHO_JSON" = true ]; then
      echo "Current Battle JSON:"
      echo "$response" | jq . 
    fi
  else
    echo "Failed to get battle started."
    exit 1
  fi
}



# Function to clear combatants

clear_combatants() {
  echo "Clearing combatants..."
  response=$(curl -s -X POST "$BASE_URL/clear-combatants")

  if echo "$response" | grep -q '"status": "combatants cleared"'; then
    echo "Combatants cleared successfully."
  else
    echo "Failed to clear playlist."
    exit 1
  fi
}


# Function to get combatants

get_combatants() {
  echo "Getting current combatants..."
  response=$(curl -s -X GET "$BASE_URL/get-combatants")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Current combatant retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Current Combatant JSON:"
      echo "$response" | jq . 
    fi
  else
    echo "Failed to retrieve current combatant."
    exit 1
  fi
}


# Function to prep a meal to become a combatant

prep_combatant() {
  meal_name=$1

  echo "Preparing combatant ($meal_name) for battle.."
  response=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"meal\": \"$meal_name\"}" "$BASE_URL/api/prep-combatant")
  if echo "$response" | grep -q '"status": "combatant prepared"'; then
    echo "Successfuly prepared combatant ($meal_name)."
  else
    echo "Failed to prepare combatant ($meal_name)."
    exit 1
  fi
}



# Function to get the meal leaderboard sorted

get_leader_board_by_wins() {
  echo "Getting leaderboard of meals sorted by wins..."
  response=$(curl -s -X GET "$BASE_URL/leaderboard?sort=wins")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Leaderboard retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal Leaderboard JSON (sorted by wins):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal leaderboard."
    exit 1
  fi
}
get_leader_board_by_battles() {
  echo "Getting leaderboard of meals sorted by wins..."
  response=$(curl -s -X GET "$BASE_URL/leaderboard?sort=battles")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Leaderboard retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal Leaderboard JSON (sorted by wins):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal leaderboard."
    exit 1
  fi
}
get_leader_board_by_win_pct() {
  echo "Getting leaderboard of meals sorted by wins..."
  response=$(curl -s -X GET "$BASE_URL/leaderboard?sort=win_pct")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Leaderboard retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal Leaderboard JSON (sorted by wins):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal leaderboard."
    exit 1
  fi
}

