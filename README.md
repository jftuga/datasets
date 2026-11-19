# datasets

Test datasets of numbers, one per line, for exercising statistics tools such as [go-stats-calculator](https://github.com/jftuga/go-stats-calculator).

| Directory | Contents |
|-----------|----------|
| [`random/`](random/) | 30 uniform or power-skewed random datasets generated with `randrange`. Documented below. |
| [`non-random/`](non-random/) | 30 simulated real-world datasets (queues, tides, seasonality, mixtures, and more). See its [README](non-random/README.md). |
| [`non_random_gen/`](non_random_gen/) | The Python generator for `non-random/`. See its [README](non_random_gen/README.md). |

## Disclaimer

All code and datasets in this repository were vibe-coded with Claude Opus 5.5. Every dataset is synthetic: none of it comes from real measurements, and the "real-world" files only simulate the processes they are named after. Do not rely on these files for research, decisions, or any purpose where accuracy matters. Everything is provided as is, without warranty of any kind (see [LICENSE](LICENSE)), and the author is not responsible for its accuracy or for how it is used.

## Random datasets

The files in `random/` were generated with [randrange](https://github.com/jftuga/randrange) v0.3.1. Each file holds one number per line. The 30 files differ in count (20 to 1,000,000), range, number type (integer or float), and distribution (uniform or skewed). Together they take about 34 MB.

### File naming

```
c<count>_s<start>_e<end>[_f][_sk<low|high><strength>].txt
```

| Part | Meaning | randrange flag |
|------|---------|----------------|
| `c<count>` | Number of values (lines) | `-count` |
| `s<start>` | Inclusive lower bound | `-start` |
| `e<end>` | Inclusive upper bound | `-end` |
| `_f` | Floats (8 decimal places) instead of integers | `-floats` |
| `_sklow<n>` | Skewed toward start, strength n | `-skew low -skew-strength n` |
| `_skhigh<n>` | Skewed toward end, strength n | `-skew high -skew-strength n` |

Example: `c25000_s-500_e500_f_skhigh3.txt` holds 25,000 floats in [-500, 500], skewed toward 500 with strength 3.

### Datasets

| File | Count | Range | Type | Skew | Size |
|------|------:|-------|------|------|-----:|
| `c20_s1_e10.txt` | 20 | 1 to 10 | int | - | 42 B |
| `c37_s-10_e10_f.txt` | 37 | -10 to 10 | float | - | 422 B |
| `c50_s0_e1_f.txt` | 50 | 0 to 1 | float | - | 550 B |
| `c75_s-100_e100_skhigh2.txt` | 75 | -100 to 100 | int | high 2 | 244 B |
| `c100_s1_e6.txt` | 100 | 1 to 6 | int | - | 200 B |
| `c150_s-1000_e0_sklow3.txt` | 150 | -1000 to 0 | int | low 3 | 762 B |
| `c250_s1_e1000000.txt` | 250 | 1 to 1,000,000 | int | - | 1.7 KB |
| `c400_s-50_e50_f_skhigh2.5.txt` | 400 | -50 to 50 | float | high 2.5 | 4.7 KB |
| `c600_s0_e255.txt` | 600 | 0 to 255 | int | - | 2.1 KB |
| `c1000_s-5_e5_f.txt` | 1,000 | -5 to 5 | float | - | 11 KB |
| `c1500_s1_e100_sklow4.txt` | 1,500 | 1 to 100 | int | low 4 | 3.6 KB |
| `c2500_s-273_e100_f.txt` | 2,500 | -273 to 100 | float | - | 32 KB |
| `c3333_s1_e52.txt` | 3,333 | 1 to 52 | int | - | 9.2 KB |
| `c5000_s1_e100.txt` | 5,000 | 1 to 100 | int | - | 14 KB |
| `c5000_s-1000000_e1000000.txt` | 5,000 | -1,000,000 to 1,000,000 | int | - | 36 KB |
| `c7500_s0_e1000_skhigh1.5.txt` | 7,500 | 0 to 1000 | int | high 1.5 | 29 KB |
| `c10000_s-1_e1_f.txt` | 10,000 | -1 to 1 | float | - | 112 KB |
| `c15000_s1_e365_sklow2.txt` | 15,000 | 1 to 365 | int | low 2 | 49 KB |
| `c25000_s-500_e500_f_skhigh3.txt` | 25,000 | -500 to 500 | float | high 3 | 319 KB |
| `c40000_s0_e65535.txt` | 40,000 | 0 to 65,535 | int | - | 228 KB |
| `c50000_s-100_e-1.txt` | 50,000 | -100 to -1 | int | - | 191 KB |
| `c75000_s1_e1000_f_sklow2.5.txt` | 75,000 | 1 to 1000 | float | low 2.5 | 912 KB |
| `c100000_s1_e1000000_sklow3.txt` | 100,000 | 1 to 1,000,000 | int | low 3 | 601 KB |
| `c150000_s-32768_e32767.txt` | 150,000 | -32,768 to 32,767 | int | - | 902 KB |
| `c200000_s0_e100_f_skhigh5.txt` | 200,000 | 0 to 100 | float | high 5 | 2.3 MB |
| `c300000_s-10000_e10000_sklow1.5.txt` | 300,000 | -10,000 to 10,000 | int | low 1.5 | 1.6 MB |
| `c500000_s1_e2147483647.txt` | 500,000 | 1 to 2,147,483,647 | int | - | 5.0 MB |
| `c600000_s-1_e1000_skhigh2.txt` | 600,000 | -1 to 1000 | int | high 2 | 2.3 MB |
| `c800000_s-1000000_e0_f.txt` | 800,000 | -1,000,000 to 0 | float | - | 13 MB |
| `c1000000_s1_e1000000.txt` | 1,000,000 | 1 to 1,000,000 | int | - | 6.6 MB |

Totals: 30 files, 10 float, 12 skewed, 14 with negative values.

### Regenerating

Requires [randrange](https://github.com/jftuga/randrange) on your `PATH`.

```bash
./generate.sh
```

`generate.sh` holds the spec table for every dataset. It creates `random/` if needed, overwrites all `random/c*.txt` files, and then prints the count, min, max, and mean of each file. To add a dataset, add a line to the heredoc in the script with this format:

```
count start end floats(f|-) skew(low|high|-) strength(n|-)
```

### Notes

- randrange has no seed option, so regenerating produces new values. The file names and parameters stay the same.
- Skew strength 1.0 is uniform; higher values concentrate values more strongly. A low skew of strength k puts the mean at roughly 1/(k+1) of the way through the range (for example, about 25% for k=3). A high skew of strength k puts it at roughly k/(k+1) (about 83% for k=5).
- High-skew float files contain the exact end value, for example 1,780 lines of `100.00000000` in `c200000_s0_e100_f_skhigh5.txt` and 5 lines of `500.00000000` in `c25000_s-500_e500_f_skhigh3.txt`. Those counts match the number of draws expected to fall within 5e-9 of the end, so this is rounding to 8 decimal places, not evidence that the float range is inclusive.
- Running `randrange` without arguments prints 5 numbers in [0, 100]. Use `randrange -h` to list its options.
