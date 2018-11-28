import pandas as pd
import datetime
import sys
import ast
import os

def load_member():
    members_data = pd.read_csv('member.csv')    #fields: memberID, issuedBooksISBN_n_Dates_dict{"ISBN":"issuing_date"}, num_books_issued
    return members_data

def load_books():
    books_data = pd.read_csv('books2.csv')
    return books_data

def check_if_member_exists(mem_id):
    members_data = load_member()
    for indexer in members_data.index:
        if members_data.iloc[indexer].memberID == mem_id:
            return True         
        else:
            return False

def check_if_isbn_present(isbn):
    present_books = load_books()    #reads the list of books from bookDS
    for indexer in present_books.index:
        if present_books.iloc[indexer].ISBN == isbn:
            return True             #book present
        else:
            return False                    #book not present

def if_book_already_issued(isbn, mem_id):
    members_data = load_member()    #reads from members.json
    for indexer in members_data.index:
        if members_data.iloc[indexer].memberID == mem_id:
            ori_entries_str = members_data.iloc[indexer, 1]
            ori_entries_dict = ast.literal_eval(ori_entries_str)
            ori_entries_dict = ast.literal_eval(ori_entries_dict)
            if isbn in ori_entries_dict:        #the book's ISBN is already present
                return False                    #therefore, cannot re-issue the same book
            else:
                return True                     #since the book's ISBN wasn't found, can be issued

def check_book_available(isbn, mem_id):
    books_data = load_books()    #reads from books2.json
    for indexer in books_data.index:
        if (books_data.ISBN[indexer] == isbn) and (int(books_data.books_count[indexer]) > 0):
            return if_book_already_issued(books_data.ISBN[indexer], mem_id)    
                    #check if the member already has the books issued to them or not
        else:
            return False

def check_member_issuing_limit(mem_id):
    members_data = load_member()    #reads from members.json
    for indexer in members_data.index:
        if (members_data.memberID[indexer] == mem_id) and (int(members_data.num_books_issued[indexer]) <= 4):
            return True
        else:
            return False

def modify_member(mem_id, book_issued):    # modify member with given id
    members_data = load_member()    #reads from members.json
    for indexer in members_data.index:
        if members_data.memberID[indexer] == mem_id:
            # member_data.iloc[indexer, 1].update(book_issued)
            ori_entries_str = members_data.iloc[indexer, 1]
            ori_entries_dict = ast.literal_eval(ori_entries_str)
            ori_entries_dict = ast.literal_eval(ori_entries_dict)
            ori_entries_dict.update(book_issued)            ####### add in the ISBN:date pair into dict
            new_entries = "\""+str(ori_entries_dict)+"\""
            # print(len(ori_entries_dict))
            members_data.iloc[indexer, 2] += 1
            # print(members_data.iloc[indexer])
            members_data.iloc[indexer, 1] = new_entries
    ###write the members_data df to csv HERE only
    members_data.to_csv('./member.csv', index = False)       #change name to that of original csv
    
def modify_book(isbn, mode):        #to be done in booksCSV after allot/return of book
    # book_count has a default value of 1 for members returning book
    # ie, a member can return only one copy of a particular book at one time
    # count = 1
    books_data = load_books()
    for indexer in books_data.index:
        # if books_data.iloc[indexer].ISBN == isbn:
        if books_data.ISBN[indexer] == isbn:
            if mode == 0:    # mode = 0 => alloting book to member
                # print("book allot")
                # print(books_data.books_count[indexer])
                books_data.books_count[indexer] -= 1    
            elif mode == 1:  # mode = 1 => accepting book from member
                # print("book return")
                # print(books_data.books_count[indexer])
                books_data.books_count[indexer] += 1
    books_data.to_csv('./books2.csv', index = False)       #change name to that of original csv
    ###write the books_data df to csv HERE only

def calculate_fine(mem_id, book_isbn):
    members_data = load_member()
    # search for member with given id and issued isbn
    return_date = 0
    issuing_date = 0
    for indexer in members_data.index:
        if members_data.iloc[indexer].memberID == mem_id:
            ori_entries_str = members_data.iloc[indexer, 1]
            ori_entries_dict = ast.literal_eval(ori_entries_str)
            ori_entries_dict = ast.literal_eval(ori_entries_dict)
            if book_isbn in ori_entries_dict:
# get issuing_date and calc return_date using datetime module
                issuing_date = ori_entries_dict[book_isbn]
                issuing_date_date = datetime.datetime.strptime(issuing_date, '%d-%m-%Y').date()      #strptime requires 'from datetime import datetime'
                return_date = datetime.datetime.strptime(datetime.datetime.now().strftime('%d-%m-%Y'), '%d-%m-%Y').date()   #now() requires 'import datetime'
                # return_date = dttm.datetime.now().strftime('%d-%m-%Y')
                # return_date_date = datetime.strptime(return_date, '%d-%m-%Y')
                break
    diff_days = (return_date - issuing_date_date).days      #calculates fine
    if diff_days > 14:
        differ = diff_days - 14
        fine_amount = (differ) * 2
        print(f"Fine amount to be paid : Rs.{fine_amount}")
    else:
        print('Book returned within 15 days.\nNo fine')

def modify_mem_on_book_return(book_isbn, mem_id):
    members_data = load_member()
    for indexer in members_data.index:
        if members_data.iloc[indexer].memberID == mem_id:
            ori_entries_str = members_data.iloc[indexer, 1]
            ori_entries_dict = ast.literal_eval(ori_entries_str)
            ori_entries_dict = ast.literal_eval(ori_entries_dict)
            if book_isbn in ori_entries_dict:
                ori_entries_dict.pop(book_isbn, None)
                new_entries = "\""+str(ori_entries_dict)+"\""
                # print(len(ori_entries_dict))
                # members_data.iloc[indexer].num_books_issued -= 1
                members_data.iloc[indexer, 2] -= 1          ##changes num_books_issued
                # print(members_data.iloc[indexer, 2])
                # print(members_data.iloc[indexer].num_books_issued)
                # print(type(members_data.iloc[indexer].num_books_issued))
                members_data.iloc[indexer, 1] = new_entries  ###write this new dict back to df and then the df to csv
    # replace old file data with new
    members_data.to_csv('./member.csv', index = False)       #change name to that of original csv

def add_member():
    try:
        memberID = int(input("Enter the NEW member's 7-digit member ID:\n"))
        if len(str(memberID)) != 7:
            print('Member ID has to be 7 digits long.')
#         else:
#             break
    except ValueError:
        print("Invalid entry...")
    else:
        if check_if_member_exists(memberID):
            print("Member with the enter ID already exists in the system.\nCannot make duplicate entry.\n")
            return
        else:
            members_data = load_member()
            new_mem = {'memberID': 0, 'issuedBooksISBN_n_Dates_dict': [{}], 'num_books_issued': 0}
            new_mem['memberID'] = memberID
            new_mem['issuedBooksISBN_n_Dates_dict'] = "\""+"{}"+"\""
            new_df = pd.DataFrame(data=new_mem, columns=['memberID', 'issuedBooksISBN_n_Dates_dict', 'num_books_issued'], index=[0])
            members_data = members_data.append(new_df, ignore_index=True)
            # print(members_data.tail())
#             WRITE IN CODE TO WRITE THE PRESENT DF TO CSV USING to_csv
            members_data.to_csv('./member.csv', index = False)

def add_book():
    # ask for parameters of a book from user
    try:
        title = input('Enter Book Title: ')
        author = input('Enter Name of Author(s): ')
#         author = input('Enter Name of Author(s): ').split(', ')
        isbn = int(input('Enter Book ISBN (12 digit ISBN is followed by this library): '))
        if len(str(isbn)) != 12:
            print('Length of ISBN has to be 12. Try again.')
        book_count_to_add = int(input('Enter number of copies of this book to be added: '))
    except ValueError:
        print('Invalid Input, ISBN/Number of copies has to be a number. Try again.')
        return
    else:
        if check_if_isbn_present(isbn):     #if check_if_isbn_present() returned TRUE
            print('Book with same ISBN and title already exists, Book details will be updated...')
            books_data = load_books()
            for indexer in books_data.index:
                if books_data.iloc[indexer].ISBN == isbn:
                    new_book = {'ISBN': 0,'title': [],'authors': [],'books_count': 0}
                    cp = books_data.iloc[indexer].books_count
                    drop_row = books_data.iloc[indexer]
                    books_data = books_data[books_data.index != indexer]
                    new_book['ISBN']= isbn
                    new_book['title'] = title
                    new_book['authors'] = author
                    new_book['books_count'] = book_count_to_add + cp
                    new_df = pd.DataFrame(data=new_book, columns=['ISBN','title','authors','books_count'], index=[0])
                    books_data = books_data.append(new_df, ignore_index=True)
        else:
            books_data = load_books()
            new_book = {'ISBN': 0,'title': [],'authors': [],'books_count': 0}
            new_book['ISBN']= isbn
            new_book['title'] = title
            new_book['authors'] = author
            new_book['books_count'] = book_count_to_add
            new_df = pd.DataFrame(data=new_book, columns=['ISBN','title','authors','books_count'], index=[0])
            books_data = books_data.append(new_df, ignore_index=True)
            # print(books_data.tail())
            #             WRITE IN CODE TO WRITE THE PRESENT DF TO CSV USING to_csv
            books_data.to_csv('./books2.csv', index = False)
    print('Book details updated in system...')

def issue_book():
    mem_id = int(input('Enter member id to whom book has to be issued : '))
    # check if member present in library records
    if check_if_member_exists(mem_id):
        # find member with given data and check if he has reached book limit
        if check_member_issuing_limit(mem_id):      # returned TRUE means book limit has not been reached and hence we can issue book
            new_book_isbn = int(input('Enter ISBN of book that has to be issued : '))
            # check if given isbn is present and num copies of it are > 0
            # also check is member has this book issued already or not
            if check_book_available(new_book_isbn, mem_id):
                # means isbn present and copies > 0
                # create a dict that will store isbn of book, and date of issue
                new_book_entry = {new_book_isbn: datetime.datetime.now().strftime('%d-%m-%Y')}
                # push created object into members issued books array
                modify_member(mem_id, new_book_entry)
                # reached here means book has been issued successfully
                print(f'Book Issued To member {mem_id}')
                # modify book details in library reduce copies
                modify_book(new_book_isbn, 0)
            else:
                # either isbn not present or all copies exhausted
                print('Book not available (all copies have been exhausted OR book has been issued already).\nTherefor, CANNOT ISSUE BOOK.')
                sys.exit()
        else:
            print('member at book-issuing-limit.\nTherefor, CANNOT ISSUE BOOK.\n')
            sys.exit()          #do something about this exit()
    else:
        print('Member not found.\nTherefor, CANNOT ISSUE BOOK.')
        sys.exit()          #do something about this exit()

def return_book():
    # ask for id
    mem_id = int(input('Enter id for member who is returning the book:\n'))
    # if present
    if check_if_member_exists(mem_id):     # proceeds if True is returned
        return_book_isbn = int(input('Enter Book ISBN To Be Returned: '))
        # check if it was issued to this id at all or not
        if not if_book_already_issued(return_book_isbn, mem_id):       #proceeds if True is returned by if_book_already_issued()
            # since book was issued,
            calculate_fine(mem_id, return_book_isbn)
            # book returned
            modify_book(return_book_isbn, 1)    # mode = 1 => returning,i.e., increment book_count for the ISBN
            modify_mem_on_book_return(return_book_isbn, mem_id)
        # else exit
        else:
            print(f"Book with ISBN: {book_isbn} has not been issued to this member.")
    # else exit
    else:
        print('member not found in database. Error.')

def search_book(mode, search_input_data):
    books_data = load_books()
    if mode == 'i':   # isbn search
        for indexer in books_data.index:
            if books_data.iloc[indexer].ISBN == search_input_data:
                # print(books_data.iloc[indexer].authors)
                print("-"*10)
                print(f"ISBN details are: \nAuthor:{books_data.iloc[indexer].authors}\nTitle:{books_data.iloc[indexer].title}\nCopies Available:{books_data.iloc[indexer].books_count}")
                print("-"*10)
            return
        print('Book not found.')
    elif mode == 't':    # title search
        for indexer in books_data.index:
            if books_data.iloc[indexer].title.lower() == search_input_data.lower():
                print(f"\nBook details are:\n")
                print("-"*10)
                print(f"Author: {books_data.iloc[indexer].authors}\nTitle: {books_data.iloc[indexer].title}\nISBN: {books_data.iloc[indexer].ISBN}\nCopies Available: {books_data.iloc[indexer].books_count}")
                print("-"*10)
            return
        print('Book not found.')
    elif mode == 'a':    # search using author's name
        flag = 0
        print(f"\nBooks by {search_input_data} are:\n")
        for indexer in books_data.index:
            if books_data.iloc[indexer].authors == search_input_data:
                print("-"*10)
                print(f"Title: {books_data.iloc[indexer].title}\nISBN: {books_data.iloc[indexer].ISBN}\nCopies Available: {books_data.iloc[indexer].books_count}")
                print("-"*10)
                flag = 1
        if flag == 0:
            print('Book not found.')

def member_issuing_details():
    members_data = load_member()  #reads from members.json
    for indexer in members_data.index:
        print("-"*10)
        print(f"memberID: {members_data.iloc[indexer].memberID}")
        print(f"Books Issued : {members_data.iloc[indexer].num_books_issued}")
        print("-"*10)

def view_all_book_details():
    books_data = load_books()     #reads from books2.json
    for indexer in books_data.index:
            print('Title : ' + books_data.iloc[indexer].title)
            print('Author : ' + books_data.iloc[indexer].authors)
            print(f"ISBN: {books_data.iloc[indexer].ISBN}")
            print(f"Copies available: {books_data.iloc[indexer].books_count}")
            print("-"*10)