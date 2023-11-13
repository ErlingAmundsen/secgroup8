#test script for statistics and privacy markers
import pandas as pd
import matplotlib.pyplot as plt

def K_anonymity(dataPrivate:pd.DataFrame):
    col = dataPrivate.columns.tolist()

    col.remove('party')
    k_anym = dataPrivate.groupby(col).size().min(skipna=True)
    return k_anym

def l_diversity(dataPrivate:pd.DataFrame):
    col = dataPrivate.columns.tolist()

    col.remove('party')
    l_div = dataPrivate.groupby(col)['party'].nunique().min(skipna=True)
    
    return l_div

def run_analysis_a(dataPrivate:pd.DataFrame, dataPublic:pd.DataFrame, dataResults:pd.DataFrame, plot_title):
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


def create_graph_b(dataPrivate:pd.DataFrame, group:str, colors:list = []):
    # get the number of people who voted in the survey grouped by gender
    red_votes = dataPrivate[dataPrivate['party'] == 'Red'].groupby(group).size().reset_index(name='count')
    green_votes = dataPrivate[dataPrivate['party'] == 'Green'].groupby(group).size().reset_index(name='count')
    invalid_votes = dataPrivate[dataPrivate['party'] == 'Invalid vote'].groupby(group).size().reset_index(name='count')

    redCounts = []
    greenCounts = []
    invalidCounts = []

    index = dataPrivate[group].unique()

    for i in index:
        total = red_votes.where(red_votes[group] == i).dropna()['count'].sum() + green_votes.where(green_votes[group] == i).dropna()['count'].sum() + invalid_votes.where(invalid_votes[group] == i).dropna()['count'].sum()
        redCounts.append(red_votes.where(red_votes[group] == i).dropna()['count'].sum()/total * 100)
        greenCounts.append(green_votes.where(green_votes[group] == i).dropna()['count'].sum()/total * 100)
        invalidCounts.append(invalid_votes.where(invalid_votes[group] == i).dropna()['count'].sum()/total * 100)


    df = pd.DataFrame({'Red': redCounts, 'Green': greenCounts, 'Invalid votes': invalidCounts}, index=index)

    rot = 0 if len(index) < 5 else 90
    if colors:
        df.plot.bar(rot=rot, color=colors)
    else:
        df.plot.bar(rot=rot)


def run_analysis_b(dataPrivate:pd.DataFrame, dataPublic:pd.DataFrame, dataResults:pd.DataFrame, plot_title):

    create_graph_b(dataPrivate, "sex", ["red", "green", "orange"])

    create_graph_b(dataPrivate, "education")
    create_graph_b(dataPrivate, "dob")
    plt.show()


def main():
    # Load the original datasets
    file_path = 'GroupG/private_dataG.xlsx'
    data_private = pd.read_excel(file_path)
    file_path = 'GroupG/public_data_registerG.xlsx'
    data_public = pd.read_excel(file_path)
    file_path = 'GroupG/public_data_resultsG.xlsx'
    data_results = pd.read_excel(file_path)

    data, plt = run_analysis_a(data_private, data_public, data_results, 'Red votes non-anonymised')
    # plt.show()
    run_analysis_b(data_private, data_public, data_results, 'Red votes non-anonymised')


if __name__ == "__main__":
    main()
