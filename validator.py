import logging
import os
from pathlib import Path


logger = logging.getLogger(__name__)


def is_valid_voltage(voltage):
    if not isinstance(voltage, (int, float)):
        raise TypeError("voltage must be numeric")

    return 11.5 <= voltage <= 12.5


def classify_temperature(temp):
    if temp < -20:
        return "TOO_LOW"
    if temp > 80:
        return "TOO_HIGH"
    return "OK"


def calculate_pass_rate(results):
    if not results:
        raise ValueError("results cannot be empty")

    passed = sum(result == "PASS" for result in results)

    return passed / len(results) * 100


def read_serial_number(path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(path)

    serial = path.read_text().strip()

    if not serial:
        raise ValueError("empty serial number")

    return serial


def get_test_environment():
    return os.environ.get("TEST_ENV", "development")


def validate_device(voltage, temperature):
    logger.info("Starting device validation")

    if not is_valid_voltage(voltage):
        logger.error("Voltage validation failed")
        return False

    if classify_temperature(temperature) != "OK":
        logger.error("Temperature validation failed")
        return False

    logger.info("Device validation passed")
    return True