"""Test module."""

from datetime import datetime
import sys
import pytest
import sqlite3

sys.path.append("../ehr_data_software_tool")  # noqa: E402
import ehr_analysis as ehr
from ehr_analysis import Patient, Lab

# assume we already have the following data
# patients = [
#     (1, "male", "1947-12-28 02:45:40.547", "white"),
#     (2, "female", "1960-01-20 04:35:40.547", "african american"),
#     (3, "male", "2000-02-13 04:35:40.547", "white"),
#     (99, "female", "2020-02-23 04:35:40.547", "asian"),
# ]
# labs = [
#     (1, 1, "lab_a", 1, "2007-12-30 02:45:40.547"),
#     (1, 1, "lab_b", 0.5, "2007-12-30 02:45:40.547"),
#     (1, 1, "lab_c", 10, "2021-12-01 02:45:40.547"),
#     (2, 1, "lab_a", 2, "2022-01-20 04:35:40.547"),
#     (2, 1, "lab_b", 0.6, "2022-01-20 04:35:40.547"),
#     (3, 1, "lab_a", 2, "2022-02-14 04:35:40.547"),
# ]

conn = sqlite3.connect("ehr.db")
c = conn.cursor()


def test_age():
    """Test property Patient.age."""
    assert round(Patient().age(c, 1)) == 74
    assert round(Patient().age(c, 2)) == 62
    assert round(Patient().age(c, 3)) == 22


def test_num_older_than():
    """Test method num_older_than."""
    assert ehr.num_older_than(c, 0) == 4
    assert ehr.num_older_than(c, 1000) == 0
    assert ehr.num_older_than(c, 50) == 2


def test_is_sick():
    """Test property Patient.is_sick."""
    assert Patient().is_sick(c=c, pid=1, aid=1, lab_name="lab_a", gt_lt=">", value=0.5)
    assert not Patient().is_sick(
        c=c, pid=2, aid=1, lab_name="lab_b", gt_lt="<", value=0.3
    )
    with pytest.raises(ValueError) as excinfo:
        Patient().is_sick(c=c, pid=1, aid=1, lab_name="lab_a", gt_lt=">=", value=0.5)
    assert "incorrect string for gt_lt" in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        Patient().is_sick(c=c, pid=1, aid=1, lab_name="lab_z", gt_lt=">", value=100)
    assert "this patient has not taken" in str(excinfo.value)


# def test_sick_patients():
#     """Test sick_patients."""
#     assert ehr.sick_patients("lab_a", ">", 1, patients_list) == {"2", "3"}
#     assert ehr.sick_patients("lab_z", ">", 0, patients_list) == set()
#     with pytest.raises(ValueError) as excinfo:
#         ehr.sick_patients("lab_a", ">=", 1, patients_list)
#     assert "incorrect string for gt_lt" in str(excinfo.value)


# def test_age_at_first_admission():
#     """Test get_age_at_first_admission."""
#     assert round(patients["1"].age_at_first_admission) == 60
#     assert round(patients["2"].age_at_first_admission) == 62
#     assert round(patients["3"].age_at_first_admission) == 22
#     with pytest.raises(AttributeError) as excinfo:
#         patients["99"].age_at_first_admission
#     assert "has not taken any lab yet" in str(excinfo.value)
