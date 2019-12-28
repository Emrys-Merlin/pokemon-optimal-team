from optimal_teams import find_optimal_teams, are_optimal_teams
import pandas as pd

def test_find_optimal_teams():
    df = pd.DataFrame([[2., 2.], [1., .5]], index=['a', 'b'], columns=['a', 'b'])

    res = find_optimal_teams(df, n_max=1)

    assert res.shape[1] == 1
    assert res.shape[0] == 1

    df = pd.DataFrame([[2., 1.], [.5, 2.]])
    res = find_optimal_teams(df, n_max=1)
    assert res.shape[1] == 1
    assert res.shape[0] == 0

    res = find_optimal_teams(df, n_max=2)
    assert res.shape[1] == 2
    assert res.shape[0] == 1

    df = pd.DataFrame([[.5, 1., 1.], [2., 2., 2.], [2., 2., 2.]])
    res = find_optimal_teams(df, seed=[0], n_max=2)
    assert res.shape[1] == 2
    assert res.shape[0] == 2

    for _, row in res.iterrows():
        assert row[0] == 0


def test_are_optimal_teams():
    df = pd.DataFrame([[2., 2.], [1., .5]])
    teams = pd.DataFrame([[0], [1]])

    res = are_optimal_teams(df, teams)
    assert len(res) == 2
    assert res[0]
    assert not res[1]

    teams = pd.DataFrame([[0, 1]])
    res = are_optimal_teams(df, teams)
    assert len(res) == 1
    assert res[0]

