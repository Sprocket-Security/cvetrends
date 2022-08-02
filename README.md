<div align="center">

# cvet

cvet is a Python utility for pulling actionable vulnerabilities from cvetrends.com

Tool checks if vulnerabilities published within the specified timeframe have more than two GitHub Repos published.

<br>

[Installation](#installation) /
[Usage](#usage)

</div><br>

</div>
<br>

## Installation

bhp supports all major operating systems and can be installed for the PyPi using the following command:

```
pipx install cvet
```

If this tool is not yet availible via PyPi, you can install it directly from the repository using:

```
git clone https://github.com/puzzlepeaches/cvetrends.git
cd cvetrends && pip3 install .
```

For development, clone the repository and install it locally using poetry.

```
git clone https://github.com/puzzlepeaches/cvetrends.git && cd cvetrends
poetry shell 
poetry install
```

<br>

## Usage

The cvet help menu is shown below:

```
 Usage: cvet [OPTIONS] [[day|week]]                                                                                              
                                                                                                                                 
 cvetrends.com CLI                                                                                                               
                                                                                                                                 
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ TIME_FRAME    [[day|week]]                                                                                                    │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --notify          -n   TEXT     Slack webhook to notify on run                                                                │
│ --repo-threshold  -rt  INTEGER  Number of repos needed to show CVE. [default: 1]                                              │
│ --help            -h            Show this message and exit.                                                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

cvet can query time frames of 24 hours or 7 days using a value of `day` or `week`. The default is `day`.

```
cvet week 
```

Results are returned in a pretty table format and only vulnerabilities that have more than `-rt` PoC GitHub repos published are shown. The default is 1.

```
cvet day -rt 2
```

cvet also allows you to specify a Slack webhook to notify on run using the `-n` or `--notify` flag. This is useful if you want to be notified of new vulnerabilities and run this tool on a cron.

```
cvet -n https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX -rt 2 -tf 24hrs
```


