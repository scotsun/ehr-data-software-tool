"""Test module."""

import sys
import pytest

sys.path.append("../ehr_data_software_tool")
if True:
    import ehr_analysis as ehr


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
    return


def test_num_older_than():
    """Test num_older_than."""
    patient_data = ehr.parse_data("./PatientCorePopulatedTable.txt")
    assert ehr.num_older_than(-999, patient_data) == 100
    assert ehr.num_older_than(1000, patient_data) == 0
    assert ehr.num_older_than(51.2, patient_data) == 77
    return


def test_sick_patients():
    """Test sick_patients."""
    test_lab_data = ehr.parse_data("./tests/test_data3.txt")
    assert ehr.sick_patients("lab1", ">", 1, test_lab_data) == set(["2", "3", "4", "5"])
    assert ehr.sick_patients("lab2", "<", 0.7, test_lab_data) == set(["1", "2"])
    assert ehr.sick_patients("lab99", "<", 99, test_lab_data) == set()
    with pytest.raises(ValueError) as excinfo:
        ehr.sick_patients("lab1", ">=", 1.5, test_lab_data) == set(["2", "3", "4", "5"])
    assert "incorrect string for gt_lt" in str(excinfo.value)
    return


def test_get_age_at_first_admission():
    """Test get_age_at_first_admission."""
    test_patient_data = ehr.parse_data("./tests/test_data4.txt")
    test_lab_data = ehr.parse_data("./tests/test_data5.txt")
    assert (
        round(ehr.get_age_at_first_admission("1", test_lab_data, test_patient_data))
        == 60
    )
    assert (
        round(ehr.get_age_at_first_admission("2", test_lab_data, test_patient_data))
        == 62
    )
    with pytest.raises(ValueError) as excinfo:
        ehr.get_age_at_first_admission("999", test_lab_data, test_patient_data)
    assert "patient ID not found in lab records" in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        ehr.get_age_at_first_admission("99", test_lab_data, test_patient_data)
    assert "patient ID not found in patient records." in str(excinfo.value)
