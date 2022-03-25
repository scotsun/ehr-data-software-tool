"""Test module."""

from os import remove
import sys
import pytest
import sqlite3
from sqlite3 import IntegrityError

sys.path.append("../ehr_data_software_tool")  # noqa: E402
import ehr_analysis as ehr
from ehr_analysis import *

try:
    remove("./test_ehr.db")
except FileNotFoundError:
    pass
conn = sqlite3.connect("test_ehr.db")
c = conn.cursor()
c.execute(
    """
    create table if not exists patients(
        [_pid] integer primary key autoincrement,
        [pid] text not null unique,
        [gender] text,
        [dob] text not null,
        [race] text
    )
    """
)

c.execute(
    """
    create table if not exists labs(
        [_lid] integer primary key autoincrement,
        [pid] text not null,
        [aid] integer not null,
        [name] text not null,
        [value] real not null,
        [date] text not null
    )
    """
)

c.execute(
    """
    create index if not exists pid_index
    on patients (pid)
    """
)

pat1 = Patient(
    cursor=c,
    pid="1",
    gender="Male",
    dob="1947-12-28 02:45:40.547",
    race="White",
)
pat2 = Patient(
    cursor=c,
    pid="2",
    gender="Female",
    dob="1960-01-20 04:35:40.547",
    race="Afican American",
)
pat3 = Patient(
    cursor=c,
    pid="3",
    gender="Male",
    dob="2000-02-13 04:35:40.547",
    race="White",
)
pat99 = Patient(
    cursor=c,
    pid="99",
    gender="Female",
    dob="2020-02-23 04:35:40.547",
    race="Asian",
)
lab1 = Lab(
    cursor=c,
    pid="1",
    aid=1,
    name="lab_a",
    value=1,
    date="2007-12-30 02:45:40.547",
)
lab2 = Lab(
    cursor=c,
    pid="1",
    aid=1,
    name="lab_b",
    value=0.5,
    date="2007-12-30 02:45:40.547",
)
lab3 = Lab(
    cursor=c,
    pid="1",
    aid=1,
    name="lab_c",
    value=10,
    date="2021-12-01 02:45:40.547",
)
lab4 = Lab(
    cursor=c,
    pid="2",
    aid=1,
    name="lab_a",
    value=2,
    date="2022-01-20 04:35:40.547",
)
lab5 = Lab(
    cursor=c,
    pid="2",
    aid=1,
    name="lab_b",
    value=0.6,
    date="2022-01-20 04:35:40.547",
)
lab6 = Lab(
    cursor=c,
    pid="3",
    aid=1,
    name="lab_a",
    value=2,
    date="2022-02-14 04:35:40.547",
)

conn.commit()


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


def test_unique_constraint():
    """Test the UNIQUE constraint of the patient table."""
    with pytest.raises(IntegrityError) as excinfo:
        Patient(
            cursor=c,
            pid="1",
            gender="Male",
            dob="1947-12-28 02:45:40.547",
            race="White",
        )
    assert "UNIQUE constraint failed" in str(excinfo.value)


def test_age():
    """Test property Patient.age."""
    assert round(pat1.age) == 74
    assert round(pat2.age) == 62
    assert round(pat3.age) == 22


def test_num_older_than():
    """Test method num_older_than."""
    pats = [pat1, pat2, pat3, pat99]
    assert ehr.num_older_than(pats, 0) == 4
    assert ehr.num_older_than(pats, 1000) == 0
    assert ehr.num_older_than(pats, 50) == 2


def test_is_sick():
    """Test property Patient.is_sick."""
    assert pat1.is_sick(aid=1, lab_name="lab_a", gt_lt=">", value=0.5)
    assert not pat2.is_sick(aid=1, lab_name="lab_b", gt_lt="<", value=0.3)
    with pytest.raises(ValueError) as excinfo:
        pat1.is_sick(aid=1, lab_name="lab_a", gt_lt=">=", value=0.5)
    assert "incorrect string for gt_lt" in str(excinfo.value)
    with pytest.raises(LabError) as excinfo:
        pat99.is_sick(aid=1, lab_name="lab_z", gt_lt=">", value=100)
    assert "this patient has not taken" in str(excinfo.value)


def test_sick_patients():
    """Test sick_patients."""
    pats = [pat1, pat2, pat3, pat99]
    assert ehr.sick_patients(patients=pats, aid=1, lab="lab_a", gt_lt=">", value=1) == {
        "2",
        "3",
    }
    assert (
        ehr.sick_patients(patients=pats, aid=1, lab="lab_z", gt_lt=">", value=0)
        == set()
    )
    with pytest.raises(ValueError) as excinfo:
        ehr.sick_patients(patients=pats, aid=1, lab="lab_a", gt_lt=">=", value=1)
    assert "incorrect string for gt_lt" in str(excinfo.value)


def test_age_at_first_admission():
    """Test get_age_at_first_admission."""
    assert round(pat1.age_at_first_admission) == 60
    assert round(pat2.age_at_first_admission) == 62
    assert round(pat3.age_at_first_admission) == 22
    with pytest.raises(LabError) as excinfo:
        pat99.age_at_first_admission
    assert "has not taken any lab yet" in str(excinfo.value)

    conn.close()
