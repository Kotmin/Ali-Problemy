import pytest
from manager import OwnerPetManager


@pytest.fixture
def manager(tmp_path):
    return OwnerPetManager(filename=tmp_path / "test_kto_ma_co.txt")


def test_save_new_owner_pet_data_success(manager):
    result = manager.save_new_owner_pet_data("Jan", "kot")
    assert "Jan ma kot" in result
    assert "od" in result


def test_save_new_owner_pet_data_missing_owner(manager):
    with pytest.raises(ValueError, match="Both 'owner' and 'pet' must be provided."):
        manager.save_new_owner_pet_data("", "kot")


def test_save_new_owner_pet_data_missing_pet(manager):
    with pytest.raises(ValueError, match="Both 'owner' and 'pet' must be provided."):
        manager.save_new_owner_pet_data("Jan", "")
