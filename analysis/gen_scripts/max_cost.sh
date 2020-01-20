# -N	počet instancí
# -n	počet věcí
# -m	poměr kapacity batohu k sumární váze
# -W	max. hmotnost věci
# -w	převaha věcí lehkých/těžkých/balanc [bal|light|heavy]
# -C	max. cena věci
# -c	korelace s hmotností žádná/menší/silná [uni|corr|strong]
# -k	granularita (pouze pokud je -w light|heavy)

path="../../data/DataAnalysis"
name="MaxCost"

mkdir -p "$path"/"$name"

../gen/kg2 -N 250 -n 15 -m 0.8 -W 250 -w bal -C 100 -c uni -k 1.0 \
>$path/$name/"$name"_100_inst.dat

../gen/kg2 -N 250 -n 15 -m 0.8 -W 250 -w bal -C 200 -c uni -k 1.0 \
>$path/$name/"$name"_200_inst.dat

../gen/kg2 -N 250 -n 15 -m 0.8 -W 250 -w bal -C 300 -c uni -k 1.0 \
>$path/$name/"$name"_300_inst.dat

../gen/kg2 -N 250 -n 15 -m 0.8 -W 250 -w bal -C 400 -c uni -k 1.0 \
>$path/$name/"$name"_400_inst.dat

../gen/kg2 -N 250 -n 15 -m 0.8 -W 250 -w bal -C 500 -c uni -k 1.0 \
>$path/$name/"$name"_500_inst.dat