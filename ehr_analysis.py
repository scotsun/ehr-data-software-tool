"""2022-01-28 Scott Sun.

Data structure chosen for data parsing is dict[str, list]
Time complexity to locate a row is O(N).
Time complexity to locate a given row's particular variable is O(1).
"""

from datetime import datetime


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
        temp = datetime.strptime(patient_dob[i], "%Y-%m-%d %H:%M:%S.%f")
        diff = now - temp
        if diff.days / 365.25 > age:
            count += 1
    return count


def sick_patients(
    lab: str, gt_lt: str, value: float, lab_records: dict[str, list[str]]
) -> list[str]:
    """Take the data and return a (unique) list of patients with the condition.

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
    return list(output)
