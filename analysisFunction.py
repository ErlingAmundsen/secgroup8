#test script for statistics and privacy markers
import pandas as pd
import matplotlib.pyplot as plt
from anonymisation import *
import numpy as np
def K_anonymity(dataPrivate:pd.DataFrame):
    col = dataPrivate.columns.tolist()

    col.remove('party')
    k_anym = dataPrivate.groupby(col).size().min(skipna=True)
    # print where k-anonymity is 1
    print(dataPrivate.groupby(col).size().where(dataPrivate.groupby(col).size() == 1).dropna())
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


def create_graph_b(dataPrivate:pd.DataFrame, group:str, target:str, targets:list, colors:list = [], target_labels:list = [], title:str = "Set title"):

    # create list of dataframes with counts for each target
    selectedItems = []
    for t in targets:
        selectedItems.append(dataPrivate[dataPrivate[target] == t].groupby(group).size().reset_index(name='count'))

    counts = {}
    # create dict with empty lists for each target
    for i in targets:
        counts[i] = []

    index = np.sort(dataPrivate[group].unique())

    # fill dict with counts
    val_sum = []
    for i in index:
        s = 0
        for j in range(len(targets)):
            val = selectedItems[j].where(selectedItems[j][group] == i).dropna()['count'].sum()
            counts[targets[j]].append(val)
            s += val
        val_sum.append(s)

    # percentage
    for i in counts:
        counts[i] = [x / y * 100 for x, y in zip(counts[i], val_sum)]

    # rename keys if target_labels is given
    if target_labels:
        counts = dict(zip(target_labels, counts.values()))

    # create dataframe from dict
    df = pd.DataFrame(counts, index=index)

    # plot dataframe
    rot = 0 if len(index) < 5 else 90
    if colors:
        df.plot.bar(rot=rot, color=colors, title = title)
    else:
        df.plot.bar(rot=rot, title=title)


def run_analysis_b(dataPrivate:pd.DataFrame):
    b_list = ["Red", "Green", "Invalid vote"]


    create_graph_b(dataPrivate, "sex", "party", b_list, ["red", "green", "orange"], title='voting dist based on sex')
    create_graph_b(dataPrivate, "education", "party", b_list, ["red", "green", "orange"],title='voting dist based on education')
    create_graph_b(dataPrivate, "dob", "party", b_list, ["red", "green", "orange"], title='voting dist based on age')

    c_list = [1,0] 
    c_label_list = ["Evote", "Regular vote"]
    create_graph_b(dataPrivate, "sex", "evote", c_list, ["red", "green"], c_label_list, 'voting channel based on sex')
    create_graph_b(dataPrivate, "education", "evote", c_list, ["red", "green"], c_label_list,'voting channel based on education')
    create_graph_b(dataPrivate, "dob", "evote", c_list, ["red", "green"], c_label_list,'voting channel based on age')

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
    run_analysis_b(anonymize(data_private))


if __name__ == "__main__":
    main()
