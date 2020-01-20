path="analysis/tester_results"
ALG="SA"

# Init temperature
echo "Initial temperature"
OUT_DIR=$path"/ParamAnalysis/InitTemperature"
step=200
start=100
end=1000

for i in `seq $start $step $end`; do 
    echo $i
    run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/$i --init-temperature $i --min-temperature 1 --cooling 0.995 --cycles 50
done

step=300
start=1000
end=3100

for i in `seq $start $step $end`; do 
    echo $i
    run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/$i --init-temperature $i --min-temperature 1 --cooling 0.995 --cycles 50
done

# # Cooling
echo "Cooling"
OUT_DIR=$path"/ParamAnalysis/Cooling"

step=15
start=815
end=995

for i in `seq $start $step $end`; do 
    echo 0.$i
    run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/0.$i --init-temperature 500 --min-temperature 1 --cooling 0.$i --cycles 50
done

# Cycles
echo "Cycles"
OUT_DIR=$path"/ParamAnalysis/Cycles"

step=25
start=100
end=250

for i in `seq $start $step $end`; do 
    echo $i
    run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/$i --init-temperature 500 --min-temperature 1 --cooling 0.995 --cycles $i
done