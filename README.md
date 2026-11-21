# NINE O'CLOCK FIELDS — The Poster for a Place That Isn't There

[![Bounty](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![Rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/turibaru/poster-place-isnt-there/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![Reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/turibaru/poster-place-isnt-there/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)

A vintage travel poster for a place that does not exist: **NINE O'CLOCK FIELDS** —
terraced golden hillsides where every footstep plays a note, so the whole
valley hums one sustained chord every night at nine o'clock. At the centre
of the valley stands the Nine O'Clock Bell, the single slender bell-tower
where all the glowing notes converge and spiral up into the violet twilight.

## The image

`entry.png` — 500×1000 px PNG, 916,782 bytes.

- SHA-256: `1a96550c98cb479cbc67d38a64366c394c00000714255f19c2759ccc85249e62`

## Run

```sh
python3 main.py
# writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output)
# and verifies the copy SHA-256 byte-for-byte
```

`main.py` uses only the Python standard library, needs no network access,
and validates the image before writing: PNG/JPEG magic bytes, size
≤ 1,048,576 bytes, dimensions ≤ 1024×1024 (parsed from IHDR/SOF).
