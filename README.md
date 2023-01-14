# Vorogoj

This project is for educational purposes only! Do NOT run this on machines other than your own.

## Setup

1. Create a `constants.py` file with the contents as specified in `constants.py.example`. The GitHub API token can be a 'fine-grained personal access token' as long as they include the 'Read and Write access to gists' permission.
2. Run `controller.py` on the botmaster machine.
3. Run `bot.py` on the client machine(s).

Note: Python 3.10 is no longer required (on Jan 14, the code was migrated from match-case to elif chains.)

## Caveats

- Multiple bots can not run on a single public IPv4 address as of now because of the IP-W3W client naming scheme.
  They would be assigned the same name and thus both run the same commands and report the results under the same filename.
