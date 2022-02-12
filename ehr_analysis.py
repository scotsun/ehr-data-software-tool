"""2022-01-28 Scott Sun.

Data structure chosen for data parsing is dict[str, list]
Time complexity to locate a row is O(N).
Time complexity to locate a given row's particular variable is O(1).
"""

from datetime import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


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


def num_older_than(age: float, patient_records: dict[str, list[str]]) -> int:
    """Take the data and return the number of patients older than a given age.

    Time complexity is O(N) as a for-loop iterate through the parsed data.

    Parameters:
    age (float): Age of interest
    patient_records (dict[str, list[str]]): Parsed data

    Returns:
    int:number of patients that fit the condition

    """
    patient_dob = patient_records["PatientDateOfBirth"]
    now = datetime.now()
    count = 0
    for i in range(len(patient_dob)):
        temp = datetime.strptime(patient_dob[i], DATE_FORMAT)
        diff = now - temp
        if diff.days / 365.25 > age:
            count += 1
    return count


def sick_patients(
    lab: str, gt_lt: str, value: float, lab_records: dict[str, list[str]]
) -> set[str]:
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
        for i in range(len(lab_records["PatientID"])):
            if (
                lab_records["LabName"][i] == lab
                and float(lab_records["LabValue"][i]) > value
            ):
                output.add(lab_records["PatientID"][i])
    elif gt_lt == "<":
        for i in range(len(lab_records["PatientID"])):
            if (
                lab_records["LabName"][i] == lab
                and float(lab_records["LabValue"][i]) < value
            ):
                output.add(lab_records["PatientID"][i])
    else:
        raise ValueError("incorrect string for gt_lt")
    return output


def get_patient_dob(patient_id: str, patient_records: dict) -> str:
    """Get patient's DOB."""
    for i in range(len(patient_records["PatientID"])):
        if patient_records["PatientID"][i] == patient_id:
            dob = patient_records["PatientDateOfBirth"][i]
            return dob
    raise ValueError("patient ID not found.")


def get_age_at_first_admission(
    patient_id: str, lab_records: dict, patient_records: dict
) -> float:
    """Calculate the age of a given patient at the first admission (based on the first lab date).

    Time complexity is O(N) as a for-loop iterate through the parsed data twice

    Parameter:
    patient_id (str): Patient ID
    lab_records (dict): Parsed data

    Returns:
    int:list of patient IDs

    """
    # get all the lab dates of the first adimission
    patient_ids = lab_records["PatientID"]
    admit_ids = lab_records["AdmissionID"]
    lab_dates = lab_records["LabDateTime"]
    nrow = len(patient_ids)
    idx_list = [
        i for i in range(nrow) if patient_ids[i] == patient_id and admit_ids[i] == "1"
    ]
    if len(idx_list) == 0:
        raise ValueError("patient ID not found.")

    # get date of the first lab
    min_date = datetime.strptime(lab_dates[idx_list[0]], DATE_FORMAT)
    for i in range(1, len(idx_list)):
        temp = datetime.strptime(lab_dates[idx_list[i]], DATE_FORMAT)
        if temp < min_date:
            min_date = temp
    # get patient dob
    dob_str = get_patient_dob(patient_id, patient_records)
    dob = datetime.strptime(dob_str, DATE_FORMAT)
    diff = min_date - dob
    age = diff.days / 365.25
    return age
