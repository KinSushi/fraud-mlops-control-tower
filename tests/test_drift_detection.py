import pandas as pd

from fraud_mlops.drift_detection import population_stability_index


def test_population_stability_index_same_distribution() -> None:
    series = pd.Series(range(100))
    psi = population_stability_index(series, series)

    assert psi == 0.0
