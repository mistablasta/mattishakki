# mattishakki
[![codecov](https://codecov.io/gh/mistablasta/mattishakki/graph/badge.svg?token=OLBMUSIGFU)](https://codecov.io/gh/mistablasta/mattishakki)

### Manual
Run the application with
```
python src/main.py (player vs player)
```
```
python src/main.py --ai (player vs ai)
```
```
python src/main.py --battle (ai vs ai)
```
All manual moves are entered in the following example format
```
e2e4 (where, to)
```
Use the --debug flag to make AI move timings visible for performance tracking.

Install project dependencies with poetry if intending to run tests.
```
poetry install
```
