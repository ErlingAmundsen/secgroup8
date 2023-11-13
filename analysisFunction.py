#test script for statistics and privacy markers
import pandas as pd
import matplotlib.pyplot as plt

def run_analysis_a(dataPrivate:pd.DataFrame, dataPublic:pd.DataFrame, dataResults:pd.DataFrame, plot_title):
    #make list of columns 
    col = dataPrivate.columns.tolist()

    col.remove('party')
    k_anym = dataPrivate.groupby(col).size().min(skipna=True)

    #percentage red votes according to survey electronic
    totalVotesElec = dataPrivate['evote'].sum()
    evotesRed = dataPrivate['party'][dataPrivate['evote'] == 1].value_counts()['Red']/totalVotesElec

    #percentage red votes according to survey normal
    totalVotesNorm = (dataPrivate['evote'] == 0).sum()
    votesRed = dataPrivate['party'][dataPrivate['evote'] == 0].value_counts()['Red']/totalVotesNorm

    #percentage red votes according to results electronic
    totalEvotesRes = dataResults['Total'][4]
    evotesRedRes = dataResults['Red'][4]/totalEvotesRes
    

    #percentage red votes according to results normal
    totalVotesRes = dataResults['Total'][5] - totalEvotesRes
    votesRedRes = dataResults['Red'][5]/totalVotesRes

    data = {
        'Regular votes': [votesRed, votesRedRes],
        'Electronic votes': [evotesRed, evotesRedRes],
        'k-anonymity': k_anym
    }
    _, axs = plt.subplots(1, 2, figsize=(6, 3))
    cols = ['Regular votes', 'Electronic votes']
    for i, (title, values) in enumerate(data.items()):
        if title in cols:
            ax = axs[i]
            ax.set_title(title)
            ax.set_ylabel('Percentage')
            ax.bar(['Survey', 'Results'], values, color=['lightblue', 'orange'])
            ax.set_ylim(0, 0.7)

    plt.suptitle(plot_title)
    plt.tight_layout()
    
    return data, plt


def main():
    # Load the original datasets
    file_path = 'GroupG/private_dataG.xlsx'
    data_private = pd.read_excel(file_path)
    file_path = 'GroupG/public_data_registerG.xlsx'
    data_public = pd.read_excel(file_path)
    file_path = 'GroupG/public_data_resultsG.xlsx'
    data_results = pd.read_excel(file_path)

    data, plt = run_analysis_a(data_private, data_public, data_results, 'Red votes non-anonymised')
    plt.show()


if __name__ == "__main__":
    main()
