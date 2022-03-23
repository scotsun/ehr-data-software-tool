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

## Setting up SQLite DB
```sh
sqlite> create table if not exists patients(
			[_pid] integer primary key autoincrement,
			[pid] text not null unique,
			[gender] text,
    		[dob] text not null,
    		[race] text
		)

sqlite> create table if not exists labs(
		[_lid] integer primary key autoincrement,
		[pid] integer not null,
		[aid] integer not null,
		[name] text not null,
		[value] real not null,
		[date] text not null
	)

sqlite> create index if not exists pid_index
    	on patients (pid)
```

### Classes
#### *`Patient`*  
`insert_patient`  
insert a row of patient into the patients table of the DB

`age`  
calculate the age of a Patient object.

`age_at_first_admission`  
calculate the age at the first admission.

`is_sick`  
check if the patient is sick based on the given criterion.

#### *`Lab`*
`insert_lab`  
insert a row of lab into the labs table of the DB

### Module features

`parse_data(filename: str) -> dict[str, list[str]]`:  
it parses the data from any *.txt file with delimiter as `\t`.

`num_older_than(c: Cursor, age: float) -> int`:  
it takes the sqlite cursor and return the number of patients older than a given age.

`sick_patients(c: Cursor, aid: int, lab: str, gt_lt: str, value: float) -> set[str]`:  
it takes the sqlite cursor and return a list of unique patients with the specified condition.


## Usage example

```python
>>> import sqlite3
>>> import ehr_analysis as ehr
>>> conn = sqlite3.connect("ehr.db")
>>> c = conn.cursor()
>>> c.execute([sql_query])
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