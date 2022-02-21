"""Test module."""

import sys
import pytest

sys.path.append("../ehr_data_software_tool")
import ehr_analysis as ehr  # noqa: E402


def test_parse_data():
    """Test parse_data function."""
    data0 = {}
    data1 = {
        "var0": ["0", "1"],
        "var1": ["True", "False"],
        "var2": ["False", "True"],
        "var3": ["True", "True"],
    }
    data2 = {"var0": [], "var1": [], "var2": [], "var3": []}
    assert ehr.parse_data("./tests/test_data0.txt") == data0
    assert ehr.parse_data("./tests/test_data1.txt") == data1
    assert ehr.parse_data("./tests/test_data2.txt") == data2


lab_records = ehr.parse_data("./tests/test_data3.txt")
patient_records = ehr.parse_data("./tests/test_data4.txt")
patients = ehr.get_all_patients(patient_records, lab_records)
patients_list = list(patients.values())


def test_print():
    """Test __str__ methods for Patient and Lab."""
    assert patients["1"].__str__() == "1"
    assert patients["2"].__str__() == "2"
    lab1 = patients["1"]._labs[0]
    assert lab1.__str__() == str((lab1._pid, lab1._aid, lab1._name))


def test_age():
    """Test property Patient.age."""
    assert round(patients["1"].age) == 74
    assert round(patients["2"].age) == 62
    assert round(patients["3"].age) == 22


def test_num_older_than():
    """Test method num_older_than."""
    assert ehr.num_older_than(-999, patients_list) == 6
    assert ehr.num_older_than(1000, patients_list) == 0
    assert ehr.num_older_than(18, patients_list) == 3


def test_is_sick():
    """Test property Patient.is_sick."""
    assert patients["1"].is_sick("lab1", ">", 0.5) is True
    assert patients["2"].is_sick("lab2", "<", 0.3) is False
    with pytest.raises(ValueError) as excinfo:
        patients["1"].is_sick("lab1", ">=", 0.5)
    assert "incorrect string for gt_lt" in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        patients["1"].is_sick("lab99", ">", 100)
    assert "this patient has not taken" in str(excinfo.value)


def test_sick_patients():
    """Test sick_patients."""
    assert ehr.sick_patients("lab1", ">", 1, patients_list) == set(["2", "3", "4", "5"])
    assert ehr.sick_patients("lab99", ">", 0, patients_list) == set()
    with pytest.raises(ValueError) as excinfo:
        ehr.sick_patients("lab1", ">=", 1, patients_list)
    assert "incorrect string for gt_lt" in str(excinfo.value)


def test_age_at_first_admission():
    """Test get_age_at_first_admission."""
    assert round(patients["1"].age_at_first_admission) == 60
    assert round(patients["2"].age_at_first_admission) == 62
    assert round(patients["3"].age_at_first_admission) == 22
    with pytest.raises(AttributeError) as excinfo:
        patients["99"].age_at_first_admission
    assert "this patient has not taken any lab yet" in str(excinfo.value)
