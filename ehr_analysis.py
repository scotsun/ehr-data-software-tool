"""2022-01-28 Scott Sun.

Assume N patients and M labs per patient on average.
"""

from datetime import datetime
from sqlite3 import Cursor


DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class Lab:
    """Lab class that takes patient ID, admission ID, lab name, lab value, and lab date."""

    def __init__(
        self, cursor: Cursor, pid: str, aid: int, name: str, value: float, date: str
    ) -> None:
        """Initialize a lab by inserting a row into the labs table."""
        query = "insert into labs (pid, aid, name, value, date) values (?, ?, ?, ?, ?)"
        self.__cursor = cursor
        self.__cursor.execute(query, (pid, aid, name, value, date))


class LabError(Exception):
    """Customized exception class raised if there is anything incorrect about labs."""

    def __init__(self, *args: object) -> None:
        """Initialize."""
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        """Output string."""
        if self.message:
            return "LabError, {0}".format(self.message)
        else:
            return "LabError has been raised."


class Patient:
    """Patient class that takes patient ID, gender, DOB, and race."""

    def __init__(
        self, cursor: Cursor, pid: str, gender: str, dob: str, race: str
    ) -> None:
        """Initialize a patient by inserting a row into the patients table."""
        self._pid = pid
        self.__cursor = cursor
        query = "insert into patients (pid, gender, dob, race) values (?, ?, ?, ?)"
        self.__cursor.execute(query, (pid, gender, dob, race))

    @property
    def pid(self) -> str:
        """Getter of Patient.pid."""
        return self._pid

    @property
    def dob(self) -> datetime:
        """Get patient's dob."""
        query = f"select dob from patients where pid = '{self._pid}'"
        self.__cursor.execute(query)
        return datetime.strptime(self.__cursor.fetchone()[0], DATE_FORMAT)

    @property
    def age(self) -> float:
        """Calculate patient's age."""
        dob = self.dob
        now = datetime.now()
        diff = now - dob
        return diff.days / 365.25

    @property
    def age_at_first_admission(self) -> float:
        """Get the age at 1st admission. Time complexity O(M)."""
        query = f"select date from labs where pid = '{self._pid}' and aid = 1"
        self.__cursor.execute(query)
        lab_dates = [
            datetime.strptime(elem[0], DATE_FORMAT) for elem in self.__cursor.fetchall()
        ]
        if len(lab_dates) == 0:
            raise LabError(f"Patient {self._pid} has not taken any lab yet.")
        min_labdate = min(lab_dates)
        dob = self.dob
        diff = min_labdate - dob
        return diff.days / 365.25

    def is_sick(self, aid: int, lab_name: str, gt_lt: str, value: float) -> bool:
        """Determine if the patient is sick based on the given criterion. Time complexity O(M)."""
        query = f"""select value from labs
        where pid = ? and aid = ? and name = ?
        """
        self.__cursor.execute(query, (self._pid, aid, lab_name))
        try:
            lab_value = self.__cursor.fetchone()[0]
        except TypeError:
            raise LabError(f"this patient has not taken the lab.")
        if gt_lt == ">":
            return lab_value > value
        elif gt_lt == "<":
            return lab_value < value
        else:
            raise ValueError(f"incorrect string for gt_lt: {gt_lt}")


def parse_data(filename: str) -> dict[str, list[str]]:
    """Parse data from .txt file.

    Let the number of variables be p.
    If p << N, the computation time complexity is O(N); otherwise, it's O(N**2)

    Parameters:
    filename (str): file path

    Returns:
    dict[str, list]:a dictionary taking variable names as keys and list[str] as values

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


def num_older_than(pateints: list[Patient], age: float) -> int:
    """Take the data and return the number of patients older than a given age.

    Time complexity is O(N) for iterating through all patients.

    Parameters:
    age (float): Age of interest
    patients (list[Patient]): List of Patient objects

    Returns:
    int:number of patients that fit the condition

    """
    count = 0
    for p in pateints:
        if p.age > age:  # O(1)
            count += 1
    return count


def sick_patients(
    patients: list[Patient], aid: int, lab: str, gt_lt: str, value: float
) -> set[str]:
    """Take the data and return a set of unique patients with the specified condition.

    Time complexity is O(M*N) for iterating through all patients.

    Parameters:
    lab (str): Lab name
    gt_lt (str): Indicating greater-than or less-than
    value (float): Value used in the comparison
    lab_records (dict): Parsed data

    Returns:
    int:list of patient IDs

    """
    output: set[str] = set()
    for p in patients:
        try:
            if p.is_sick(aid, lab, gt_lt, value):  # O(M)
                output.add(p.pid)
        except LabError:
            continue
    return output
