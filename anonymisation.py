import pandas as pd
from datetime import datetime

# 2. Generalize Date of Birth to Age Groups
def bin_age(data_private):
        current_year = datetime.now().year
        data_private['dob'] = data_private['dob'].apply(lambda x: current_year - x.year)  # Converting DOB to age
        data_private['dob'] = data_private['dob'].apply(lambda x: x - x % 10)  # Grouping ages into 10 year groups
        return data_private

# 3. Transform Education
def bin_education(data_private):
        groups = {'Not stated': 'Primary education',  
        'Bachelors programmes': 'University degree',
        'Masters programmes': 'University degree',
        'PhD programmes': 'University degree'}
        data_private.replace({'education': groups}, inplace=True)
        return data_private

# 4. Change Nationality to other
def bin_citezenship(data_private):
        data_private['citizenship'] = data_private['citizenship'].apply(lambda x: 'Other' if x != 'Denmark' else x)
        return data_private

def anonymize():
        # Load the original datasets
        file_path = 'GroupG/private_dataG.xlsx'  
        data_private = pd.read_excel(file_path)

        # Analyzing the original k-anonymity
        original_re_identification_columns = ['name', 'sex', 'dob', 'zip', 'education', 'citizenship', 'marital_status', 'party']
        original_k_anonymity_groups = data_private.groupby(original_re_identification_columns).size()
        original_k_anonymity = original_k_anonymity_groups.min()

        # remove name
        data_private.drop('name', axis=1, inplace=True)

        # 2. Generalize Date of Birth to Age Groups
        data_private = bin_age(data_private)

        # 3. Transform Education
        data_private = bin_education(data_private)

        # 4. generalise citizenship
        data_private = bin_citezenship(data_private)
        
        return data_private

def main():
        data_private = anonymize()
        print(data_private)

if __name__ == "__main__":
        main()
