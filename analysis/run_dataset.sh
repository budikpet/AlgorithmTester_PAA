ALG="SA_SAT_V3"
CONC="Files"
RESULTS_DIR="tester_results_TEST"

init_temp=1000
min_temp=0.5
cycles=50
cooling=0.95

# wufA

PARENT="wuf-A"
DATASET="wuf20-88-A"
run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/$RESULTS_DIR/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling --max-retry-attempts 3