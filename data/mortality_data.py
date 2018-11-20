import pandas as pd
import time
import math

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def fileter_text(notes):
    for note in notes.iterrows():


def get_note(notes, subject_id):
    notes = notes.loc[notes["HADM_ID"] == subject_id]
    if "TEXT" in notes.columns:
        return filter_text(notes["TEXT"])
    else:
        return None


def get_time(row):
    admit_time = time.strptime(row[1]["ADMITTIME"], TIME_FORMAT)
    death_time = time.strptime(row[1]["DEATHTTIME"], TIME_FORMAT)
    time_left = (death_time - death_time).days
    return time_left

def create_dataset(admissions, notes):
    dataset = dict()
    count = 0
    for row in admissions.iterrows():
        ID = row[1]["HADM_ID"]
        note = get_note(notes, ID)
        if note is None:
            continue

        dataset[count] = {}
        dataset[count]["HADM_ID"] = ID #"SUBJECT_ID"
        mortality = row[1]["DEATHTIME"]
        if math.isnan(mortality):
            dataset[count]['MORTALITY'] = 0
            dataset[count]['mortality_TIME'] = -1
        else:
            dataset[count]['MORTALITY'] = 1
            time = get_time(row)
            dataset[count]['MORTALITY_TIME'] = time

        dataset[count]['note'] = get_note(notes, dataset[count]["HADM_ID"])
        count+=1

def main():
    mimic_dataset_dir = "/mnt/data1/mimic_iii/mimic_data"
    notes_dataset = "/NOTEEVENTS.csv"
    admissions_dataset = "/ADMISSIONS.csv"

    admissions = pd.read_csv(mimic_dataset_dir + admissions_dataset)
    notes = pd.read_csv(mimic_dataset_dir + notes_dataset)
    final_df = create_dataset(admissions, notes)

if __name__ == "__main__":
    main()
