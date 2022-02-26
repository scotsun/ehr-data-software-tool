"""2022-01-28 Scott Sun.

Data structure chosen for data parsing is dict[str, list]
Time complexity to locate a row is O(N).
Time complexity to locate a given row's particular variable is O(1).

Assume N patients and M labs per patient on average.
"""

from datetime import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class Lab:
    """Lab class that takes patient ID, admission ID, lab name, lab value, and lab date."""

    def __init__(
        self, pid: str, aid: str, name: str, value: float, date: datetime
    ) -> None:
        """Initialize."""
        self._pid = pid
        self._aid = aid
        self._name = name
        self._value = value
        self._date = date

    def __str__(self) -> str:
        """__str__ method."""
        prime_key = (self._pid, self._aid, self._name)
        return str(prime_key)

    @property
    def pid(self) -> str:
        """Get patient ID."""
        return self._pid

    @property
    def aid(self) -> str:
        """Get patient ID."""
        return self._aid

    @property
    def name(self) -> str:
        """Get patient ID."""
        return self._name


class Patient:
    """Patient class that takes patient ID, gender, DOB, and race."""

    def __init__(self, pid: str, gender: str, dob: datetime, race: str) -> None:
        """Initialize."""
        self._pid = pid
        self._gender = gender
        self._dob = dob
        self._race = race
        self._labs: list[Lab] = []

    def __str__(self) -> str:
        """__str__ method."""
        return self._pid

    @property
    def pid(self) -> str:
        """Get patient ID."""
        return self._pid

    @property
    def labs(self) -> list[Lab]:
        """Get labs."""
        return self._labs

    @property
    def age(self) -> float:
        """Calculate patient's age."""
        now = datetime.now()
        diff = now - self._dob
        return diff.days / 365.25

    @property
    def age_at_first_admission(self) -> float:
        """Get the age at 1st admission. Time complexity O(M)."""
        if len(self._labs) == 0:
            raise AttributeError(f"Patient {self.pid} has not taken any lab yet.")
        min_labdate = self._labs[0]._date
        for lab in self._labs:
            if lab._aid == "1" and lab._date < min_labdate:
                min_labdate = lab._date
        diff = min_labdate - self._dob
        return diff.days / 365.25

    def takes_lab(self, lab: Lab) -> None:
        """Append the lab object into Patient._lab. Time complexity O(1)."""
        if self.pid != lab.pid:
            raise ValueError(f"Lab {str(lab)} does not match patient {self.pid}.")
        self._labs.append(lab)

    def is_sick(self, lab_name: str, gt_lt: str, value: float) -> bool:
        """Determine if the patient is sick based on the given criterion. Time complexity O(M)."""
        for lab in self._labs:
            if gt_lt == ">":
                if lab._name == lab_name:
                    return lab._value > value
            elif gt_lt == "<":
                if lab._name == lab_name:
                    return lab._value < value
            else:
                raise ValueError(f"incorrect string for gt_lt: {gt_lt}")
        raise AttributeError(f"this patient has not taken lab {lab_name}")


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


def get_all_patients(
    patient_records: dict[str, list[str]], lab_records: dict[str, list[str]]
) -> dict[str, Patient]:
    """Re-parse data from the dictionaries into Lab and Patient objects.

    Time complexity O(N + M*N)

    Parameters:
    patient_records (dict[str, list[str]]): patient dict
    lab_records (dict[str, list[str]): lab dict

    Returns:
    dict[str, Patient]:a dictionary taking pids as keys and Patient objects as values
    """
    num_pats = len(patient_records["PatientID"])
    patients: dict[str, Patient] = dict()
    for i in range(num_pats):
        pid = patient_records["PatientID"][i]
        patient = Patient(
            pid=pid,
            gender=patient_records["PatientGender"][i],
            dob=datetime.strptime(
                patient_records["PatientDateOfBirth"][i], DATE_FORMAT
            ),
            race=patient_records["PatientRace"][i],
        )
        patients[pid] = patient  # O(1)

    num_labs = len(lab_records["PatientID"])
    for i in range(num_labs):
        pid = lab_records["PatientID"][i]
        lab = Lab(
            pid=pid,
            aid=lab_records["AdmissionID"][i],
            name=lab_records["LabName"][i],
            value=float(lab_records["LabValue"][i]),
            date=datetime.strptime(lab_records["LabDateTime"][i], DATE_FORMAT),
        )
        patients[pid].takes_lab(lab=lab)  # O(1)
    return patients


def num_older_than(age: float, patients: list[Patient]) -> int:
    """Take the data and return the number of patients older than a given age.

    Time complexity is O(N) for iterating through all patients.

    Parameters:
    age (float): Age of interest
    patients (list[Patient]): List of Patient objects

    Returns:
    int:number of patients that fit the condition

    """
    count = 0
    for patient in patients:
        if patient.age > age:  # O(1)
            count += 1
    return count


def sick_patients(
    lab: str, gt_lt: str, value: float, patients: list[Patient]
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
    for patient in patients:
        try:
            if patient.is_sick(lab_name=lab, gt_lt=gt_lt, value=value):  # O(M)
                output.add(patient.pid)
        except AttributeError as e:
            if "this patient has not take" in e.args[0]:
                continue
    return output
