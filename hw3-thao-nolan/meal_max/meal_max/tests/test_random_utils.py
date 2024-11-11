import pytest
import requests 
from meal_max.utils.random_utils import get_random

RANDOM_NUMBER = 0.42

@pytest.fixture
def mock_random_org(mocker):
    # Patch the requests.get call
    # requests.get returns an object, which we have replaced with a mock object
    mock_response = mocker.Mock()
    # We are giving that object a text attribute
    mock_response.text = f"{RANDOM_NUMBER}"
    mocker.patch("requests.get", return_value=mock_response)
    return mock_response

def test_get_random(mock_random_org):
    """Test retrieving a random number from random.org."""
    result = get_random()

    # Assert that the result is the mocked random number
    assert result == RANDOM_NUMBER, f"Expected random number {RANDOM_NUMBER}, but got {result}"

    # Ensure that the correct URL was called
    requests.get.assert_called_once_with("https://www.random.org/integers/?num=1&min=1&max=100&col=1&base=10&format=plain&rnd=new", timeout=5)


def test_get_random_get_invalid_responses(mocker) : 
    """Simulate  an invalid response (non-digit)."""
    mock_random_org.text = "invalid_response"
    with pytest.raises(ValueError, match="Invalid response from random.org: invalid_response"):
        get_random()

    
def test_get_random_get_invalid_requests(mocker) : 
    """Simulate  a request failure."""
    mocker.patch("requests.get", side_effect=requests.exceptions.RequestException("Connection error"))

    with pytest.raises(RuntimeError, match="Request to random.org failed: Connection error"):
        get_random()

