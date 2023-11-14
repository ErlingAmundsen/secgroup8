import pandas as pd
def main():
    # Load the original datasets
    file_path = 'GroupG/private_dataG.xlsx'
    data_private = pd.read_excel(file_path)

    # Create auxillary data
    auxillary_data = data_private[["name", "zip", "marital_status", "citizenship", "dob"]]

    # Save auxillary data
    auxillary_data.to_csv("GroupG/auxillary_dataG.csv", index=False)
if __name__ == "__main__":
    main()