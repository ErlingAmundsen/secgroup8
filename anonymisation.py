import pandas as pd
from datetime import datetime

# 2. Generalize Date of Birth to Age Groups
def bin_age(data_private):
        current_year = datetime.now().year
        data_private['dob'] = data_private['dob'].apply(lambda x: current_year - x.year)  # Converting DOB to age
        bins = [0, 18, 30, 40, 50, 60, 70, 80, 90, 100]
        labels = ['<18', '18-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90+']
        data_private['age_group'] = pd.cut(data_private['dob'], bins=bins, labels=labels, right=False)
        data_private.drop('dob', axis=1, inplace=True)  # Removing the original age column
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

def main():
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

if __name__ == "__main__":
        main()
