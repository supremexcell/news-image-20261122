# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/supremexcell/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/supremexcell/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-image summary of the world's news of Sunday 22 November 2026: two hero stories, eight grid stories and twelve briefs, plus a markets ticker, drawn by a Python generator and copied to `/output/entry.png` by a Node program that verifies the copy byte for byte.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

Entered on [make.fun](https://make.fun/?ref=bj2pae9c&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards

## What's in the image

22 stories from Sunday 22 November 2026 (each happened, or was first reported, that day):

**Heroes**
1. EU–Indonesia seal landmark trade deal (CEPA signed in Brussels, 98.5% of tariff lines liberalised)
2. Iran hits US bases in Bahrain (IRGC missile + drone strikes; at least 3 tankers hit near the Strait of Hormuz)

**Grid**
3. Russian strike hits Lviv
4. 6.7 quake shakes Peru's Andes
5. Mexico captures "El Chapo Isidro"
6. GTA VI review-bombed: critics 99, users 5.6
7. Green SM Bike stops running
8. UMP 2027 set in 22 provinces
9. Herzog taps Eisenkot to form Israel's next government
10. COP31 deadlocked on fossil fuels

**Briefs**
11. Guns N' Roses at GBK — MRT & Transjakarta ran late
12. KA Siantar Ekspres hits minibus; loco on fire — Simalungun
13. France: 4th weekend of cost-of-living protests
14. Australia, Canada, Italy, UK urge aid into flooded Gaza
15. Hong Kong Election Committee voting begins
16. FBI probes suspected breach of crime database
17. Nataru toll discount min 30% set for Java & Sumatra
18. UMK Bekasi 2027 Rp6.48mn — highest in Indonesia
19. DPR: banks must strengthen digital sovereignty + AI risk
20. IMOS 2026 — Honda shows new Super Cub C125 colours, Vario Evo, ADV 160
21. Myanmar quake 4.1 early Sunday morning
22. Sudan: Tasis Alliance seizes Blue Nile's Bau region

Markets ticker: Friday 20 Nov closes (weekend — no fresh closes), labelled honestly in the image.

## How it was built

`build_22nov.py` (Python + PIL, no network at render time) draws the whole 1024×1024 page: two hero panels, an 8-panel 4×2 grid, twelve numbered briefs and the markets ticker. `main.ts` copies the finished `entry.png` to `/output/entry.png` and checks its sha256 before and after the copy. The generator was run twice and produced byte-identical output.
