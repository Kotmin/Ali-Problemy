from datetime import datetime


class OwnerPetManager:
    def __init__(self, filename='Kto_ma_co.txt'):
        self.filename = filename

    def save_new_owner_pet_data(self, owner: str, pet: str):
        """
        Saves owner and pet data to a file with the current date.
        """
        if not owner or not pet:
            raise ValueError("Both 'owner' and 'pet' must be provided.")

        current_date = datetime.now().strftime('%Y-%m-%d')
        data = f"{owner} ma {pet} od {current_date}"

        with open(self.filename, 'w') as file:
            file.write(data)
        return data
