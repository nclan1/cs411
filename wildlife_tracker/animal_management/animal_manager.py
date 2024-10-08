from typing import Optional, Any, List

from wildlife_tracker.animal_management.animal import Animal


class AnimalManager:

    def __init__(self) -> None:
        animals: dict[int, Animal] = {}

    def get_animal_by_id(self, animal_id: int) -> Optional[Animal]:
        pass

    def register_animal(self, Animal) -> None:
        pass

    def remove_animal(self, animal_id: int) -> None:
        pass
    
    def get_animal_details(animal_id) -> dict[str, Any]:
        pass
    def update_animal_details(animal_id: int, **kwargs: Any) -> None:
        pass
    
    def get_animal_by_id(animal_id: int) -> Optional[Animal]:
        pass
    def get_animals_in_habitat(habitat_id: int) -> List[Animal]:
        pass
    def assign_animals_to_habitat(animals: List[Animal]) -> None:
        pass
    
