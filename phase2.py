import pandas as pd


def dob_to_age(dob):
    """Converts date of birth to age in years."""
    # dob is in datetime format
    today = pd.Timestamp("today")

    return today.year - dob.year


def age_binning(age):
    """Bins ages into 20 year groups 0-100."""
    if age < 20:
        return "0-20"
    elif age < 40:
        return "20-40"
    elif age < 60:
        return "40-60"
    elif age < 80:
        return "60-80"
    else:
        return "80-100"


# group widowed and divorced into single category
def marital_status(status):
    if status == "Widowed":
        return "Divorced/widowed"

    if status == "Divorced":
        return "Divorced/Widowed"
    else:
        return status


def main():
    publicData = pd.read_excel("opposing/public_register.xlsx")
    anonymizedData = pd.read_csv("opposing/anon_data.csv")
    targets = pd.read_csv("opposing/aux_data.csv")

    # extract public data on targets
    targets = targets.merge(publicData, on="name", how="left")

    targets["evote"] = targets["last_voted"]
    targets.drop(["last_voted"], axis=1, inplace=True)

    targets["citizenship"] = targets["citizenship"].apply(
        lambda x: "Non-Danish" if x != "Denmark" else "Danish"
    )

    targets["age"] = targets["dob"].apply(dob_to_age)
    targets["age"] = targets["age"].apply(age_binning)

    targets = targets.drop(columns=["dob"])

    targets["marital_status"] = targets["marital_status"].apply(marital_status)

    # Number of unique rows in anonymized data
    # print(targets.sex.value_counts())
    # print(anonymizedData.sex.value_counts())

    # Loop through anonymized data and add name if only one match else no match
    # import counter dic

    targetsClean = targets.drop(columns=["name"])
    anymClean = anonymizedData.drop(columns=["education"])

    common_entries = pd.merge(
        targetsClean, anymClean, how="inner", on=list(targetsClean.columns)
    )

    # Make a col for each party
    common_entries["green"] = common_entries["party"].apply(
        lambda x: 1 if x == "Green" else 0
    )
    common_entries["red"] = common_entries["party"].apply(
        lambda x: 1 if x == "Red" else 0
    )
    common_entries["invalid"] = common_entries["party"].apply(
        lambda x: 1 if x == "Invalid vote" else 0
    )
    common_entries = common_entries.drop(columns=["party"])

    # Group by different demographics and get party distribution
    grouped = (
        common_entries.groupby(targetsClean.columns.tolist())
        .agg({"green": "sum", "red": "sum", "invalid": "sum"})
        .reset_index()
    )

    revealed = targets.merge(grouped, on=targetsClean.columns.tolist(), how="left")

    # probability of being
    revealed["prob_red"] = revealed["red"] / (
        revealed["red"] + revealed["green"] + revealed["invalid"]
    )
    revealed["prob_green"] = revealed["green"] / (
        revealed["red"] + revealed["green"] + revealed["invalid"]
    )
    revealed["prob_invalid"] = revealed["invalid"] / (
        revealed["red"] + revealed["green"] + revealed["invalid"]
    )

    revealed["most_likely"] = revealed[["prob_red", "prob_green", "prob_invalid"]].max(
        axis=1
    )

    print(revealed.head())

    correct_identifications = revealed["most_likely"].sum()
    sure_identifications = revealed[revealed["most_likely"] == 1].shape[0]

    print(f"Surely identified {sure_identifications} out of {len(revealed)} records")
    print(
        f"With most likely guess we identified {int(correct_identifications)} out of {len(revealed)} records"
    )

    revealed.to_csv("revealed.csv")


if __name__ == "__main__":
    main()
