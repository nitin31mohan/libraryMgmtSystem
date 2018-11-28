import argparse
import sys
from libMGR import add_book, add_member, issue_book, return_book, member_issuing_details, view_all_book_details, search_book

task_index = 0
date_index = 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="libms")
    parser.add_argument("libms", help="libms options[-aM|-aB|-A|-R|-sI|-sT|-sA|-lAM|-lAB]", nargs=1)
    			#aM = add_member()
    			#aB = add_book() ...to DB
    			#A = issue_book()
    			#R = return_book()
    			#sI = search_book(ISBN), sT = search_book(title), sA = search_book(authorName)
    			#lAM = member_issuing_details()
    			#lB = view_all_book_details()
    parser.add_argument("-aM", help="'libms -aM' asks for new member\'s 7-digit ID and adds to system", action = "store_true")
    parser.add_argument("-aB", help="'libms -aB' asks for new book\'s Title, AuthorName, ISBN and Quantity", action = "store_true")
    parser.add_argument("-A", help="'libms -A' asks for existing member\'s ID, the to-be-allotted book\'s ISBN and allots the book to the member", action = "store_true")
    parser.add_argument("-R", help="'libms -R' asks for existing member\'s ID, the to-be-returned book\'s ISBN and returns the book to the system", action = "store_true")
    parser.add_argument("-sI", help="'libms -sI' asks for book\'s ISBN and searches for it in the system", action = "store_true")
    parser.add_argument("-sT", help="'libms -sT' asks for book\'s Title and searches for it in the system", action = "store_true")
    parser.add_argument("-sA", help="'libms -sA' asks for book\'s authorName and searches for it in the system", action = "store_true")
    parser.add_argument("-lAM", help="'libms -lAM' lists ALL members in the system and the books allotted to them", action = "store_true")
    parser.add_argument("-lAB", help="'libms -lB' lists ALL books in the system and their details", action = "store_true")
    
    args = parser.parse_args()
    if args.aM:
    	add_member()
    elif args.aB:
    	add_book()
    elif args.A:
    	issue_book()
    elif args.R:
    	return_book()
    elif args.sI:
    	search_book('i', book_ISBN)			#'i' implies 'search-by-ISBN'
    elif args.sT:
        search_book('t', book_ISBN)			#'t' implies 'search-by-title'
    elif args.sA:
    	search_book('a', book_ISBN)			#'a' implies 'search-by-authorName'
    elif args.lAM:
    	member_issuing_details()
    elif args.lAB:
    	view_all_book_details()