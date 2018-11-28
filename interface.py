from libMGR import add_book, add_member, issue_book, return_book, member_issuing_details, view_all_book_details, search_book

def main_menu():
    # Library Main Menu
    print('1. Add a member to library.')
    print('2. Add a book to library.')
    print('3. Issue book to member.')
    print('4. Return book by member')
    print('5. Search for a book in library.')
    print('6. Print member issuing history.')
    print('7. Print book details')

def search_menu():
    print('1. Search book by ISBN.')
    print('2. Search book by title.')
    print('3. Search book by author.')

def get_choice():
    return int(input('Enter the choice (b/w 1 & 7) OR Press -1 to exit: '))

def search_choice_getter():
    return int(input('Enter the choice (b/w 1 & 3) OR Press -1 to exit: '))

def main():
    main_menu()
    choice = get_choice()

    while choice != -1:
        if choice == 1:
            add_member()	#done
            main_menu()
        elif choice == 2:
            add_book()
            main_menu()
        elif choice == 3:
            issue_book()
            main_menu()
        elif choice == 4:
            return_book()
            main_menu()
        elif choice == 5:
            search_menu()
            while True:
                try:
                    srch_choice = search_choice_getter()
                    break
                except ValueError:
                    print('Invalid Input. Try again.')
            while srch_choice != -1:
                if srch_choice == 1:    #chose to search by isbn
                    try:
                        book_ISBN = int(input('Enter ISBN: '))
                    except ValueError:
                        print('Invalid Input, Enter A number.')
                    else:
                        search_book('i', book_ISBN)			#'i' implies 'search-by-ISBN'
                elif srch_choice == 2:  #chose to search by title
                    try:
                        book_ISBN = input('Enter Title of book: ')
                    except ValueError:
                        print('Invalid Input.')
                    else:
                        search_book('t', book_ISBN)			#'t' implies 'search-by-title'
                elif srch_choice == 3:  #chose to search by author's name
                    try:
                        book_ISBN = input('Enter Author Name: ')
                    except ValueError:
                        print('Invalid Input.')
                    else:
                        search_book('a', book_ISBN)			#'a' implies 'search-by-authorName'
                else:
                    print('Invalid input. Enter choice for search again.')
                search_menu()   
                srch_choice = search_choice_getter()
        elif choice == 6:
            member_issuing_details()
            main_menu()
        elif choice == 7:
            view_all_book_details()
            main_menu()
        elif choice == 8:
            remove_book()
            main_menu()
        else:
            print('Invalid choice, Enter choice again.')
            main_menu()
        choice = get_choice()


if __name__ == "__main__":
    main()

    ##ADD DECORATOR logger