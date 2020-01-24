from package_parsers.knapsack_parser import KnapsackParser

def test_get_num_of_instances():
    knapsack_parser: KnapsackParser = KnapsackParser()

    with open("tests/test_parsers/fixtures/instance_files/NK10_inst.dat") as instance_file:
        count = knapsack_parser.get_num_of_instances(None, instance_file)

    assert count is not None
    assert count == 500

    print