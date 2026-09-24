import pytest
from random import random
from pathlib import Path
from validator import is_valid_voltage, classify_temperature, calculate_pass_rate, read_serial_number, get_test_environment, validate_device

path_to_create = Path(__file__).parent / "dummy_module_fixture_use.txt"



@pytest.fixture
def random_first_evens_list():
    random_len = int(random() * 100)
    return [i * 2 for i in range(random_len + 1)]

@pytest.fixture(scope="module", autouse=True)
def random_first_evens_lists():
    path_to_create.touch()
    path_to_create.write_text(str(int(random() * 100)))
    yield
    path_to_create.unlink()

@pytest.mark.smoke
def test_can_import_pathlib():
    import pathlib
    assert pathlib.Path is not None

@pytest.mark.smoke
def test_can_create_file(tmp_path):
    import pathlib
    path = tmp_path / "smoke.txt"
    path.touch()
    assert path.exists(), f"File {path} was not created"
    path.unlink()


    

def test_example():
    pass

def test_2_is_even():
    assert 2 % 2 == 0

def test_pytest_exceptions():
    with pytest.raises(ZeroDivisionError):
        print(1 / 0)


@pytest.mark.parametrize(
        "n, n_squared",
        [(1, 1), (2, 4), (3, 9), pytest.param(6, 35, marks=pytest.mark.xfail)]
)
def test_parameterized(n, n_squared):
    try:
        with open(path_to_create, "r") as f:
            print("Random value inside dummy file is: ", f.readline())
    except Exception as e:
        pytest.fail()        
    
    assert n ** 2 == n_squared

def test_random_evens_are_evens(random_first_evens_list):
    for elem in random_first_evens_list:
        assert elem % 2 == 0

### Voltage Validation Tests ###

@pytest.mark.parametrize(
        "voltage",
        [11.5, 12.5, 12, 11.9, 12.277]
)
def test_valid_voltage_succeeds(voltage):
    assert is_valid_voltage(voltage), f"A valid value of {voltage} for voltage was wrongfully rejected"

@pytest.mark.parametrize(
        "voltage",
        ["12V", None, [12]]
)
def test_wrongly_typed_voltage_triggers_type_error(voltage):
    with pytest.raises(TypeError, match="numeric"):
        is_valid_voltage(voltage)


@pytest.mark.parametrize(
        "voltage",
        [11.49, 12.59, 122, 111.9, 13.277]
)
def test_invalid_voltage_fails(voltage):
    assert not is_valid_voltage(voltage), f"An invalid value of {voltage} for voltage was wrongfully accepted"

@pytest.mark.parametrize(
        "temp",
        [0, 1, 2, -19, 79, 80, -20, 12.3, -0.77]
)
def test_valid_temperature_classified_as_ok(temp):
    assert classify_temperature(temp) == "OK", f"A valid value of {temp} for temperature was wrongfully rejected"

def test_tmp_path(tmp_path):
    path = tmp_path / "dummy_file.txt"
    path.write_text("DEV-12345\n")
    actual_value = None
    try:
        actual_value = read_serial_number(path)
        assert actual_value == "DEV-12345"
    except FileNotFoundError as e:
        pytest.fail(f"Could not read from file in tmp_path because of Exception {e}")
        




