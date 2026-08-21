# American Civil War Reading Collection

This collection applies the existing selection–queue–editor workflow to the American Civil War. Its source catalog contains 480 engagements dated from 1861 through 1865.

## Organization

- The selector operates at the individual battle or engagement level.
- Processed entries are grouped into one reading editor for each year, 1861–1865.
- Source dates, locations, CWSAC ratings, outcomes, notes, and Wikipedia links are retained.
- Theater and campaign classifications can be added later without replacing the stable source catalog.

## Processing a selection

1. Open `select_battles.html` and export `american_civil_war_processing_queue.json`.
2. Run:

   ```bash
   python3 practice/american_civil_war/manage.py process ~/Downloads/american_civil_war_processing_queue.json
   ```

## Source

- [Wikipedia: List of American Civil War battles](https://en.wikipedia.org/wiki/List_of_American_Civil_War_battles)
- Related primary-text collection: [马克思、恩格斯论美国内战](../marxist_classics/american_civil_war/README.md)

Wikipedia is a working catalog rather than a final historical authority. Disputed classifications and casualty information should be checked against specialist sources during later editorial development.

## Future work
- Add theater and campaign classifications to the source catalog.
- Add a reading editor for each theater or campaign.
- Add a reading editor for the entire war, with a timeline and map of engagements.

## References
[CWSAC: Civil War Sites Advisory Commission](https://www.nps.gov/civilwar/cwsac.htm)
[Wikipedia: List of American Civil War battles](https://en.wikipedia.org/wiki/List_of_American_Civil_War_battles)
[Wikipedia: American Civil War casualties](https://en.wikipedia.org/wiki/American_Civil_War_casualties)
[Wikipedia: American Civil War casualties by state](https://en.wikipedia.org/wiki/American_Civil_War_casualties_by_state)
[ChatGPT: American Civil War 2026-08-17 6:52 AM](https://chat.deepseek.com/a/chat/s/b484a871-4868-4d25-8b05-65aaaad38294)
[DeepSeek: American Civil War 2026-08-17 6:52 AM](https://chat.deepseek.com/a/chat/s/b484a871-4868-4d25-8b05-65aaaad38294)