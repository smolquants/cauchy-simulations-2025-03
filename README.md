# cauchy-simulations-2025-03

Economic simulations of Cauchy liquidity profile for [Spline](https://github.com/SplineFinance/abis).

## Install

Clone the repo

```sh
git clone https://github.com/smolquants/cauchy-simulations-2025-03.git
```

Install dependencies with [uv](https://github.com/astral-sh/uv) and [`ape`](https://github.com/ApeWorX/ape)

```sh
uv build
uv run ape plugins install .
uv pip install --find-links dist cauchy-simulations
```

## Run

cli

```sh
uv run python
>>> import cauchy_simulations
```

jupyter

```sh
uv run --with jupyter jupyter lab
```
