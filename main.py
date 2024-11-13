from utils.utils import ROOT_DIR, word_tokenize, stopwords, ps, stem_index

from src.reuters import Reuters
from src.spimi import SPIMI

from src.query import Query, AndQuery, OrQuery

import argparse



parser = argparse.ArgumentParser(description="Configure Reuters parser and set document limit per block.")

parser.add_argument("-d", "--docs", type=int, help="documents per block", default=500)
parser.add_argument("-r", "--reuters", type=int, help="number of Reuters files to parse, choice from 1 to 22", choices=range(1, 23), default=22)
parser.add_argument("-rs", "--remove-stopwords", action="store_true", help="remove stopwords", default=False)
parser.add_argument("-s", "--stem", action="store_true", help="stem terms", default=False)
parser.add_argument("-c", "--case-folding", action="store_true", help="use case folding", default=False)
parser.add_argument("-rn", "--remove-numbers", action="store_true", help="remove numbers", default=False)
parser.add_argument("-a", "--all", action="store_true", help="use all compression techniques", default=False)

args = parser.parse_args()

if __name__ == '__main__':

    if args.all:
        args.remove_stopwords = True
        args.stem = True
        args.case_folding = True
        args.remove_numbers = True

    """
    Upon initialization, downloads Reuters files if they're not downloaded, and stores them in a list.
    """
    reuters = Reuters(
        num_files=args.reuters,
        docs_per_block=args.docs,
        remove_stopwords=args.remove_stopwords,
        stem=args.stem,
        case_folding=args.case_folding,
        remove_numbers=args.remove_numbers
    )

    """
    Upon initialization, makes the Reuters object tokenize the files mentioned above, and stores them in a variable.
    Also creates the output directory if it hasn't been initialized.
    """
    spimi = SPIMI(reuters=reuters)

    index = spimi.construct_index()

    print("Index has been constructed.")


    while True:
        user_input = input("Would you like to conduct an AND query or an OR query? Hit enter for no. [and/or] ")
        if user_input == "":
            break
        elif user_input.lower() in ["and", "or"]:
            and_query = AndQuery(index)
            or_query = OrQuery(index)
            user_query = Query.ask_user()
            if user_input.lower() == "and":
                and_query.execute(user_query)
                and_query.print_results()
            elif user_input.lower() == "or":
                or_query.execute(user_query)
                or_query.print_results()