"""2022-01-28 Scott Sun.

Data structure chosen for data parsing is dict[str, list]
Time complexity to locate a row is O(N).
Time complexity to locate a given row's particular variable is O(1).
"""

from datetime import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class Lab:
    """Lab class."""

    def __init__(
        self, pid: str, aid: str, name: str, value: float, date: datetime
    ) -> None:
        """Initialize."""
        self._pid = pid
        self._aid = aid
        self._name = name
        self._value = value
        self._date = date


class Patient:
    """Patient class."""

    def __init__(self, pid: str, gender: str, dob: datetime, race: str) -> None:
        """Initialize."""
        self._pid = pid
        self._gender = gender
        self._dob = dob
        self._race = race
        self._labs: list[Lab] = []

    @property
    def age(self) -> float:
        """Calculate patient's age."""
        now = datetime.now()
        diff = now - self._dob
        return diff.days / 365.25

    def takes_lab(self, lab: Lab) -> None:
        """Take lab."""
        self._labs.append(lab)

    @property
    def age_at_first_admission(self) -> float:
        """Get the age at 1st admission."""
        if len(self._labs) == 0:
            raise AttributeError("this patient has not taken any lab yet.")
        min_labdate = self._labs[0]._date
        for lab in self._labs:
            if lab._aid == "1" and lab._date < min_labdate:
                min_labdate = lab._date
        diff = min_labdate - self._dob
        return diff.days / 365.25


def parse_data(filename: str) -> dict[str, list[str]]:
    """Parse data from .txt file.

    Let the number of variables be p.
    If p << N, the computation time complexity is O(N); otherwise, it's O(N**2)

    Parameters:
    filename (str): Description of arg1

    Returns:
    dict[str, list]:a dictionary that variable names as keys and values as lists

    """
    with open(filename, mode="r", encoding="utf-8-sig") as f:
        lines = f.readlines()

        if len(lines) == 0:
            return {}

        var_names = lines[0]
        var_names_list = var_names.strip().split("\t")
        dataframe: dict[str, list[str]] = {}
        for var in var_names_list:
            dataframe[var] = []

        for i in range(1, len(lines)):
            line_data_list = lines[i].strip().split("\t")
            for j in range(len(var_names_list)):
                dataframe[var_names_list[j]].append(line_data_list[j])
    return dataframe


def num_older_than(age: float, patients: list[Patient]) -> int:
    """Take the data and return the number of patients older than a given age.

    Time complexity is O(N) as a for-loop iterate through the parsed data.

    Parameters:
    age (float): Age of interest
    patients (list[Patient]): List of Patient objects

    Returns:
    int:number of patients that fit the condition

    """
    count = 0
    for i in range(len(patients)):
        if patients[i].age > age:
            count += 1
    return count


def sick_patients(lab: str, gt_lt: str, value: float, labs: list[Lab]) -> set[str]:
    """Take the data and return a set of unique patients with the specified condition.

    Time complexity is O(N) as a for-loop iterate through the parsed data.

    Parameters:
    lab (str): Lab name
    gt_lt (str): Indicating greater-than or less-than
    value (float): Value used in the comparison
    lab_records (dict): Parsed data

    Returns:
    int:list of patient IDs

    """
    output: set[str] = set()
    if gt_lt == ">":
        for i in range(len(labs)):
            temp_lab = labs[i]
            if temp_lab._name == lab and temp_lab._value > value:
                output.add(temp_lab._pid)
    elif gt_lt == "<":
        for i in range(len(labs)):
            temp_lab = labs[i]
            if temp_lab._name == lab and temp_lab._value < value:
                output.add(temp_lab._pid)
    else:
        raise ValueError("incorrect string for gt_lt")
    return output
