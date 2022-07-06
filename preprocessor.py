import pandas as pd


def preprocess(df, regions_df):
    # filtering rows
    df = df[df['Season'] == 'Summer']
    # mering NOC with regions
    df = df.merge(regions_df, on="NOC", how="left")
    # removing duplicates
    df.drop_duplicates(inplace=True)
    # cleaning data
    df.drop("ID", axis=1, inplace=True)
    df.drop("notes", axis=1, inplace=True)
    df.drop("Season", axis=1, inplace=True)
    df['Medal'].fillna('DNW', inplace=True)
    df.rename(columns={"region": "Country"}, inplace=True)
    df.drop("Games", axis=1, inplace=True)
    # Encoding medals
    df = pd.concat([df, pd.get_dummies(df["Medal"])], axis=1)
    df.drop("DNW", inplace=True, axis=1)

    return df


def w_preprocess(df, regions_df):
    # filtering rows
    df = df[df['Season'] == 'Winter']
    # mering NOC with regions
    df = df.merge(regions_df, on="NOC", how="left")
    # removing duplicates
    df.drop_duplicates(inplace=True)
    # cleaning data
    df.drop("ID", axis=1, inplace=True)
    df.drop("notes", axis=1, inplace=True)
    df.drop("Season", axis=1, inplace=True)
    df['Medal'].fillna('DNW', inplace=True)
    df.rename(columns={"region": "Country"}, inplace=True)
    df.drop("Games", axis=1, inplace=True)
    # Encoding medals
    df = pd.concat([df, pd.get_dummies(df["Medal"])], axis=1)
    df.drop("DNW", inplace=True, axis=1)

    return df

