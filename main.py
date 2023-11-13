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
    
    data, graph = run_analysis_a(data_private, data_public, data_results, 'Red votes non-anonymised')
    data['k_anonymity'] = K_anonymity(data_private)
    data['l_diversity'] = l_diversity(data_private)

    data_private_anym = anonymize(data_private)

    #with these 4 cols removed the k-anonymity is 2 and l-diversity is 2 as well
    #data_private_anym = data_private_anym.drop(['marital_status', 'dob', 'education','zip'], axis=1)
    data_anym, graph_anym = run_analysis_a(data_private_anym, data_public, data_results, 'Red votes anonymised')
    data_anym['k_anonymity'] = K_anonymity(data_private_anym)
    data_anym['l_diversity'] = l_diversity(data_private_anym)

    print('k-anonymity of original data:', data['k_anonymity'])
    print('k-anonymity of anonymised data:', data_anym['k_anonymity'])

    print('l-diversity of original data:', data['l_diversity'])
    print('l-diversity of anonymised data:', data_anym['l_diversity'])

    plt.show()
if __name__ == "__main__":
    main()