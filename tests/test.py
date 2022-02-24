"""Test module."""

from datetime import datetime
import sys
import pytest

sys.path.append("../ehr_data_software_tool")  # noqa: E402
import ehr_analysis as ehr
from ehr_analysis import Patient, Lab

pat1 = Patient(
    pid="1",
    gender="Male",
    dob=datetime.strptime("1947-12-28 02:45:40.547", ehr.DATE_FORMAT),
    race="White",
)
pat2 = Patient(
    pid="2",
    gender="Female",
    dob=datetime.strptime("1960-01-20 04:35:40.547", ehr.DATE_FORMAT),
    race="Afican American",
)
pat3 = Patient(
    pid="3",
    gender="Male",
    dob=datetime.strptime("2000-02-13 04:35:40.547", ehr.DATE_FORMAT),
    race="White",
)
pat99 = Patient(
    pid="99",
    gender="Female",
    dob=datetime.strptime("2020-02-23 04:35:40.547", ehr.DATE_FORMAT),
    race="Asian",
)
lab1 = Lab(
    pid="1",
    aid="1",
    name="lab_a",
    value=1,
    date=datetime.strptime("2007-12-30 02:45:40.547", ehr.DATE_FORMAT),
)
lab2 = Lab(
    pid="1",
    aid="1",
    name="lab_b",
    value=0.5,
    date=datetime.strptime("2007-12-30 02:45:40.547", ehr.DATE_FORMAT),
)
lab3 = Lab(
    pid="1",
    aid="1",
    name="lab_c",
    value=10,
    date=datetime.strptime("2021-12-01 02:45:40.547", ehr.DATE_FORMAT),
)
lab4 = Lab(
    pid="2",
    aid="1",
    name="lab_a",
    value=2,
    date=datetime.strptime("2022-01-20 04:35:40.547", ehr.DATE_FORMAT),
)
lab5 = Lab(
    pid="2",
    aid="1",
    name="lab_b",
    value=0.6,
    date=datetime.strptime("2022-01-20 04:35:40.547", ehr.DATE_FORMAT),
)
lab6 = Lab(
    pid="3",
    aid="1",
    name="lab_a",
    value=2,
    date=datetime.strptime("2022-02-14 04:35:40.547", ehr.DATE_FORMAT),
)
pat1.takes_lab(lab1)
pat1.takes_lab(lab2)
pat1.takes_lab(lab3)
pat2.takes_lab(lab4)
pat2.takes_lab(lab5)
pat3.takes_lab(lab6)
patients = dict()
for pat in [pat1, pat2, pat3, pat99]:
    patients[pat.pid] = pat
patients_list = patients.values()


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


def test_print():
    """Test __str__ methods for Patient and Lab."""
    assert str(patients["1"]) == "1"
    assert str(patients["2"]) == "2"
    lab1 = patients["1"].labs[0]
    assert str(lab1) == str((lab1.pid, lab1.aid, lab1.name))


def test_age():
    """Test property Patient.age."""
    assert round(patients["1"].age) == 74
    assert round(patients["2"].age) == 62
    assert round(patients["3"].age) == 22


def test_num_older_than():
    """Test method num_older_than."""
    assert ehr.num_older_than(0, patients_list) == 4
    assert ehr.num_older_than(1000, patients_list) == 0
    assert ehr.num_older_than(50, patients_list) == 2


def test_is_sick():
    """Test property Patient.is_sick."""
    assert patients["1"].is_sick("lab_a", ">", 0.5)
    assert not patients["2"].is_sick("lab_b", "<", 0.3)
    with pytest.raises(ValueError) as excinfo:
        patients["1"].is_sick("lab_a", ">=", 0.5)
    assert "incorrect string for gt_lt" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        patients["1"].is_sick("lab_z", ">", 100)
    assert "this patient has not taken" in str(excinfo.value)


def test_sick_patients():
    """Test sick_patients."""
    assert ehr.sick_patients("lab_a", ">", 1, patients_list) == {"2", "3"}
    assert ehr.sick_patients("lab_z", ">", 0, patients_list) == set()
    with pytest.raises(ValueError) as excinfo:
        ehr.sick_patients("lab_a", ">=", 1, patients_list)
    assert "incorrect string for gt_lt" in str(excinfo.value)


def test_age_at_first_admission():
    """Test get_age_at_first_admission."""
    assert round(patients["1"].age_at_first_admission) == 60
    assert round(patients["2"].age_at_first_admission) == 62
    assert round(patients["3"].age_at_first_admission) == 22
    with pytest.raises(AttributeError) as excinfo:
        patients["99"].age_at_first_admission
    assert "has not taken any lab yet" in str(excinfo.value)
