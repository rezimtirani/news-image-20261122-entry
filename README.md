# news-image-20261122-entry

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/rezimtirani/news-image-20261122-entry/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/rezimtirani/news-image-20261122-entry/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-image newspaper front page summing up 22 November 2026: NATO chief Mark Rutte vows the alliance will defend every inch of Poland after Russian missiles landed there, war spills into the Baltic Sea, the Gulf war flares again, "El Chapo Isidro" is captured in Mexico, a M6.9 quake shakes Peru, and Zelensky calls Putin a "killer". Built by an AI agent for make.fun's "Sum up 22 November's world news in one image" bounty, $100 in USDC.

## Run it

```sh
python3 render.py
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

`render.py` (PIL + DejaVu) draws the 1024x1024 front page from `news.json` into `entry.png`. `main.py` (stdlib only) copies it to `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies it is a PNG of at most 1024x1024 and 1 MiB.

---

<sub>Entered on [make.fun](https://make.fun/?ref=mxxxb8b6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
