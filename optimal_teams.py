import pandas as pd
from itertools import combinations
from tqdm import tqdm

# Multiplier indicating an effective attack in the attribute table
GOOD_MULT = 2.

def find_optimal_teams(attribute_table, seed = [], n_max = 6):
    '''Finds a team such that for each type a pokemon has advantage against it

    :name attribute_table: Table containing advantage and disadvantage of types. Attackers are assumed to be the rows
    :name seed: Specify types that have to be included in the team
    :name n_max: How many types at most do you want in the optimal team
    :return: Data frame containing a team per row
    '''
    result = pd.DataFrame(columns = range(n_max))
    df = attribute_table.copy()

    # remove all columns and rows that are covered by the seed
    for name in seed:
        for defender in df.loc[name, df.loc[name] == GOOD_MULT].index:
            df.drop(defender, axis=1, inplace=True)
        df.drop(name, axis=0, inplace=True)

    if len(seed) > n_max:
        raise Exception('You have specified more seed types than the maximal number of types in your team')
    elif len(seed) == n_max:
        if len(df.columns) == 0:
            row = pd.Series(seed)
            result = result.append(row, ignore_index=True)
        return result

    n_max -= len(seed)
    for candidate in tqdm(combinations(df.index.values.tolist(), n_max)):
        if df.loc[candidate, :].max(axis=0).sum() == GOOD_MULT*len(df.columns):
            row = pd.Series(seed + list(candidate))
            result = result.append(row, ignore_index=True)

    return result

def are_optimal_teams(attribute_table, teams):
    '''Check if a given team of types is optimal

    :name attribute_table: Pandas data frame containing the advantage disadvantae of types. Attackers are assumed tobe the tows
    :name teams: Pandas data frame containing one team per row
    :return: Boolean Pandas series with indexing of the team input
    '''
    res = pd.Series(index=teams.index)
    for i, team in teams.iterrows():
        res[i] = attribute_table.loc[team, :].max(axis=0).sum() == GOOD_MULT*len(attribute_table.columns)

    return res

if __name__ == '__main__':
    n_max = 7

    df = pd.read_csv('./attribute_table_sword_shield.csv', index_col=0)

    res = find_optimal_teams(df, n_max=n_max)
    print(res)

    res.to_csv(f'optimal_teams_n{n_max:02d}.csv')
    # res = pd.read_csv(f'optimal_teams_n{n_max:02d}.csv', index_col=0)

    print(are_optimal_teams(df, res))
