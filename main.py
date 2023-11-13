from anonymisation import *
from analysisFunction import * 

def main():
    # Load the original datasets
    file_path = 'GroupG/private_dataG.xlsx'
    data_private = pd.read_excel(file_path)
    file_path = 'GroupG/public_data_registerG.xlsx'
    data_public = pd.read_excel(file_path)
    file_path = 'GroupG/public_data_resultsG.xlsx'
    data_results = pd.read_excel(file_path)

    data, plt = run_analysis_a(data_private, data_public, data_results, 'Red votes non-anonymised')
   #plt.show()
    data_private_anym = anonymize()
    data_anym, plt_anym = run_analysis_a(data_private_anym, data_public, data_results, 'Red votes anonymised')
    #plt_anym.show()
    print(data)
    print(data_anym)

if __name__ == "__main__":
    main()