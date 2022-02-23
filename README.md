# EHR Data Analysis Tool
> A suite of software tools for parsing/searching/analyzing electronic health record (EHR) data

[![prog-status](https://img.shields.io/badge/status-in%20progress-brightgreen?style=plastic)](https://shields.io/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


## Installation

Clone the repository from GitHub.

```sh
git clone https://github.com/scotsun/EHR_data_software_tool.git
```

## API Description

Currently, the package has 2 classes and 4 module features.

### Classes
#### `Patient`  
it takes attrs: `pid`, `gender`, `dob`, `race`

`age`  
it is a property calculating the age of a Patient object.

`age_at_first_admission`  
it is a property calculating the.

`takes_lab`
it is a class method that put a `Lab` object into `Patient._labs`.

`is_sick`
it is a class method that check if the patient is sick based on the given criterion.

#### `Lab`
it takes attrs: `pid`, `aid`, `name`, `value`, `date` 

### Module features

`parse_data(filename: str) -> dict[str, list[str]]`:  
it parses the data from any *.txt file with delimiter as `\t`.

`num_older_than(age: float, patient_records: dict) -> int`:  
it takes the data and return the number of patients older than a given age.

`sick_patients(lab: str, gt_lt: str, value: float, lab_records: dict) -> set[str]`:  
it takes the data and return a list of unique patients with the specified condition.


## Usage example

```python
>>> import ehr_analysis as ehr
>>> dat = ehr.parse('./tests/test_data3.txt')
>>> print(dat)
{'PatientID': ['1', '1', '1', '2', '2', '3', '3', '4', '5', '5'], 'LabName': ['lab1', 'lab2', 'lab3', 'lab1', 'lab2', 'lab1', 'lab3', 'lab1', 'lab1', 'lab2'], 'LabValue': ['1', '0.5', '10', '2', '0.6', '2', '11', '3', '3', '0.9']}
```

## Testing
Several testing text files and a `test.py` script are created in test folder. To check test results, run either one of the following commands in the terminal after `cd` into the repo folder.

```sh
pytest ./tests/test.py
```

```sh
pytest --cov=ehr_analysis ./tests/test.py
```

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -m 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request