import argparse

def read_cmd_line_args():
    help_epilog = """Specify correct distance:
           Metrics for unrooted trees:
           ms - the Matching Split metric,
           rf - the Robinson-Foulds metric,
           pd - the Path Difference metric,
           qt - the Quartet metric,
           um - the UMAST metric,
           wrf - the Weighted Robinson-Foulds metric,
           Metrics for rooted trees:
           mc - the Matching Cluster metric,
           rc - the Robinson-Foulds metric based on clusters,
           ns - the Nodal Splitted metric with L2 norm,
           tt - the Triples metric,
           mp - the Matching Pair metric.
           mt - the RMAST metric."""

    ###############################
    # read args from command line #
    ###############################
    def restricted_int_factory(min_value, max_value):
        def restricted_int(value):
            ivalue = int(value)
            if ivalue < min_value or ivalue > max_value:
                raise argparse.ArgumentTypeError(
                    f"Wartość {ivalue} nie mieści się w zakresie {min_value}-{max_value}"
                )
            return ivalue

        return restricted_int

    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog=help_epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    # 1. Wstępny parser tylko dla -r
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("-r", action="store_true")
    pre_args, remaining_argv = pre_parser.parse_known_args()
    # 2. Wybór minimalnej wartości na podstawie -r
    MIN_UNROOTED = 5
    MIN_ROOTED = 4
    MIN_N = MIN_ROOTED if pre_args.r else MIN_UNROOTED
    MAX_N = 1000
    MIN_GEN_TREES = 1
    MAX_GEN_TREES = 100000
    group_rooted = parser.add_mutually_exclusive_group(required=True)
    group_rooted.add_argument("-r", action="store_true")
    group_rooted.add_argument("-u", action="store_true")
    group_binary = parser.add_mutually_exclusive_group(required=True)
    group_binary.add_argument("-b", action="store_true")
    group_binary.add_argument("-a", action="store_true")
    group_yule = parser.add_mutually_exclusive_group(required=True)
    group_yule.add_argument("-e", type=restricted_int_factory(MIN_GEN_TREES, MAX_GEN_TREES))
    group_yule.add_argument("-y", type=restricted_int_factory(MIN_GEN_TREES, MAX_GEN_TREES))
    parser.add_argument("-d", choices=['ms', 'rf', 'pd', 'qt', 'um', 'm3', 'wrf', 'mc', 'rc', 'ns', 'tt', 'mp', 'mt'],
                        nargs='+', required=True)
    parser.add_argument("-n", type=restricted_int_factory(MIN_N, MAX_N), required=True)
    args = parser.parse_args()
    leaves_count: int = args.n
    are_trees_yule: str = "y" if args.y else "e"
    trees_count: int = args.y if args.y else args.e
    distances: list[str] = args.d
    are_trees_binary: str = "r" if args.r else "u"
    are_trees_rooted: str = "b" if args.b else "a"
    # print(f"Args: {args}\nCommand Line: {sys.argv}\nUsed distances: {args.d}\nGenerated trees: {args.n}")
    # print(f"Dict format: {vars(args)}")
    return leaves_count, are_trees_yule, trees_count, distances, are_trees_binary, are_trees_rooted
