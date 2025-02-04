# 🥔 Spuds for SteamGifts

Temporary workaround to sync reduced/no CV games for the ESGST add-on.
Data come from the SteamGifts [bundle games](https://www.steamgifts.com/bundle-games) page.

## Usage

1. Download this [file](dist/esgst_data.zip) to your computer
2. Visit https://www.steamgifts.com/account/settings/profile?esgst=restore
3. Select Games and Games → Main
4. Select Settings to update the last reduced/no CV games sync timestamp.
5. (IMPORTANT) Select Merge
6. (Optional) Select Backup to...
7. Select Restore from Computer...
8. Browse to the downloaded `esgst_data.min.json` file
9. When asked, "Are you sure you want to restore the selected data?", select Yes.

### Caveats

Currently, there is no tracking mechanism.
If the reduced or no CV date is removed from SteamGifts, the corresponding data may not be removed from the ESGST add-on.

In the tooltip of Reduced and No CV game categories, the date format and timezone are `2025-01-16 UTC` (UTC time) instead of `Jan 16, 2025` (local time).
ESGST stores these dates as local time.
Since our timezones differ, the data file will supply date in UTC time and let JavaScript do its magic.

## Data file generation

If you want to generate the data file on your local machine, please follow this section.

Requirements: Python 3.12. Other Python versions aren't supported.

Install runtime dependencies:\
`pip install -U -r requirements.txt`

Optionally, install development dependencies:\
`pip install -U -r requirements_dev.txt`

Run the script:\
`python rncv.py`

## Credits

I take inspiration from the following repositories:

- https://github.com/rafaelgomesxyz/esgst-server
- https://github.com/rafaelgomesxyz/esgst
