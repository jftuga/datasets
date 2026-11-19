#!/usr/bin/env bash
# Generates the randrange test datasets into the random/ subdirectory from the spec table below.
# Each spec line is: count start end floats(f|-) skew(low|high|-) strength(-|n).
# Output files are named c<count>_s<start>_e<end>[_f][_sk<skew><strength>].txt and
# are overwritten if they already exist. A summary of n/min/max/mean is printed at the end.

set -euo pipefail
outdir="$(dirname "$0")/random"
mkdir -p "$outdir"
cd "$outdir"

while read -r c s e f k st; do
    name="c${c}_s${s}_e${e}"
    args=(-count "$c" -start "$s" -end "$e")
    if [[ $f == f ]]; then
        name+="_f"
        args+=(-floats)
    fi
    if [[ $k != - ]]; then
        name+="_sk${k}${st}"
        args+=(-skew "$k" -skew-strength "$st")
    fi
    randrange "${args[@]}" >| "$name.txt"
done <<'EOF'
5000 1 100 - - -
20 1 10 - - -
37 -10 10 f - -
50 0 1 f - -
75 -100 100 - high 2
100 1 6 - - -
150 -1000 0 - low 3
250 1 1000000 - - -
400 -50 50 f high 2.5
600 0 255 - - -
1000 -5 5 f - -
1500 1 100 - low 4
2500 -273 100 f - -
3333 1 52 - - -
5000 -1000000 1000000 - - -
7500 0 1000 - high 1.5
10000 -1 1 f - -
15000 1 365 - low 2
25000 -500 500 f high 3
40000 0 65535 - - -
50000 -100 -1 - - -
75000 1 1000 f low 2.5
100000 1 1000000 - low 3
150000 -32768 32767 - - -
200000 0 100 f high 5
300000 -10000 10000 - low 1.5
500000 1 2147483647 - - -
600000 -1 1000 - high 2
800000 -1000000 0 f - -
1000000 1 1000000 - - -
EOF

for f in c*.txt; do
    awk -v f="$f" 'NR==1{mn=mx=$1} {s+=$1; if($1<mn)mn=$1; if($1>mx)mx=$1} END{printf "%-36s n=%-8d min=%-16s max=%-16s mean=%.3f\n", f, NR, mn, mx, s/NR}' "$f"
done | sort -t= -k2 -n
