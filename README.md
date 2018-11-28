Library Management System Command line tool.

Created using Python3.6 alongwith libraries such as pandas, datetime, ast, and argparse. Among these, only the pandas modules is required to be installed by the user.

Can be operated using the CLI or interface files included herewith.
-aM|-aB|-A|-R|-sI|-sT|-sA|-lAM|-lB

The project makes use of 2 CSV files as basis for reference and record keeping with regards to the members registered in the system, as well as the books that are available for procurement by said members.  


Upon the ADDITION OF A NEW USER to the system, the new member's ID is added to the member.csv file.  
This new member has no books allottd to their name originally.
          ">python3 libMGRcli.py libms -aM"

Upon the ADDITION OF A NEW BOOK to the system, the new book's Title, name of the book's author, its ISBN, and the number of books to be added are added to the books2.csv file.
          ">python3 libMGRcli.py libms -aB"
  
When an existing member is issued a particular book, the member's details reflect the allotment of the book and the issuing date as a dictionary key-value pair, and increments the count for the books issued to the member.
          ">python3 libMGRcli.py libms -A"

When an existing member returns a particular book, the member's details reflect the return of the book by removing the book's ISBN from the user's records, and goes onto calculate the intended fine amount for book specified. Also, decrements the count for the books issued to the member.  
          ">python3 libMGRcli.py libms -R"
  
Books can be searched in the system using either the book's ISBN, or its Title, or AuthorName.  
          ">python3 libMGRcli.py libms -sI"
          ">python3 libMGRcli.py libms -sT"
          ">python3 libMGRcli.py libms -sA"
          
The issuing details for ALL users can be listed.
          ">python3 libMGRcli.py libms -lAM"

The details for ALL books in the system, including their Title, AuthorName, ISBN, and count can be listed.
          ">libms -lAB"
          
And, for the help menu,
          ">python3 libMGRcli.py libms --help"
