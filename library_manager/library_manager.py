import json
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

with open('books.json', 'r') as file:
    books = json.load(file)

def display_books():
    print("\n" + Fore.CYAN + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + "{:^50}".format("LIBRARY CATALOG"))
    print(Fore.CYAN + "=" * 50 + "\n")
    for i, book in enumerate(books, 1):
        title = book['Title']
        status = book['Read Status']
        read_status = Fore.GREEN + "Read" if status else Fore.RED + "UnRead"
        title_color = Fore.WHITE + Style.BRIGHT if status else Fore.YELLOW
        print(f"{Fore.BLUE}{i}. {title_color}{title} - {read_status}")
    print("\n" + Fore.CYAN + "=" * 50)
    back = input(Fore.MAGENTA + "Press Enter to go back to the main menu")

def add_book():
    print(Fore.CYAN + "\n----- Add New Book -----")
    title = input(Fore.YELLOW + "Enter the title of the book: " + Fore.WHITE)
    author = input(Fore.YELLOW + "Enter the author of the book: " + Fore.WHITE)
    genre = input(Fore.YELLOW + "Enter the genre of the book: " + Fore.WHITE)
    read_status = input(Fore.YELLOW + "Is the book read? (y/n): " + Fore.WHITE)
    if read_status.lower() == "y":
        read_status = True
    else:
        read_status = False
    books.append({"Title": title, "Author": author, "Genre": genre, "Read Status": read_status})
    print(Fore.GREEN + "Book added successfully")
    back = input(Fore.MAGENTA + "Press Enter to go back to the main menu")

def remove_book():
    print(Fore.CYAN + "\n----- Remove Book -----")
    title = input(Fore.YELLOW + "Enter the title of the book: " + Fore.WHITE)
    for book in books:
        if title.lower() in book['Title'].lower():
            read_status = Fore.GREEN + "Read" if book['Read Status'] else Fore.RED + "UnRead"
            print(f"{Fore.GREEN}Book found: {Fore.WHITE + Style.BRIGHT}{book['Title']} - {read_status}")
            confirm = input(Fore.YELLOW + "Are you sure you want to remove this book? (y/n): " + Fore.WHITE)
            if confirm.lower() == "y":
                books.remove(book)
                print(Fore.GREEN + "Book removed successfully")
                back = input(Fore.MAGENTA + "Press Enter to go back to the main menu")
                return
            else:
                print(Fore.YELLOW + "Book not removed")
                back = input(Fore.MAGENTA + "Press Enter to go back to the main menu")
                return
    print(Fore.RED + "Book not found")
    back = input(Fore.MAGENTA + "Press Enter to go back to the main menu")

def search_book():
    print(Fore.CYAN + "\n----- Search Book -----")
    title = input(Fore.YELLOW + "Enter the title of the book: " + Fore.WHITE)
    found = False
    for book in books:
        if title.lower() in book['Title'].lower():
            found = True
            read_status = Fore.GREEN + "Read" if book['Read Status'] else Fore.RED + "UnRead"
            author_info = f"{Fore.BLUE}Author: {Fore.WHITE}{book['Author']}"
            genre_info = f"{Fore.BLUE}Genre: {Fore.WHITE}{book['Genre']}"
            print(f"{Fore.GREEN}Book found: {Fore.WHITE + Style.BRIGHT}{book['Title']} - {read_status}")
            print(author_info)
            print(genre_info)
    
    if not found:
        print(Fore.RED + "Book not found")
    
    back = input(Fore.MAGENTA + "Press Enter to go back to the main menu")

def display_statistics():
    print(Fore.CYAN + "\n----- Library Statistics -----")
    total_books = len(books)
    read_books = sum(1 for book in books if book['Read Status'])
    unread_books = total_books - read_books
    
    if total_books > 0:
        read_percentage = (read_books/total_books*100)
    else:
        read_percentage = 0
    
    print(f"{Fore.BLUE}Total books: {Fore.WHITE + Style.BRIGHT}{total_books}")
    print(f"{Fore.GREEN}Read books: {Fore.WHITE + Style.BRIGHT}{read_books}")
    print(f"{Fore.RED}Unread books: {Fore.WHITE + Style.BRIGHT}{unread_books}")
    print(f"{Fore.YELLOW}Percentage of books read: {Fore.WHITE + Style.BRIGHT}{read_percentage:.1f}%")
    back = input(Fore.MAGENTA + "Press Enter to go back to the main menu")

def mark_as_read():
    print(Fore.CYAN + "\n----- Mark Book as Read -----")
    title = input(Fore.YELLOW + "Enter the title of the book: " + Fore.WHITE)
    for book in books:
        if title.lower() in book['Title'].lower():
            read_status = Fore.GREEN + "Read" if book['Read Status'] else Fore.RED + "UnRead"
            print(f"{Fore.GREEN}Book found: {Fore.WHITE + Style.BRIGHT}{book['Title']} - {read_status}")
            
            if book['Read Status']:
                print(Fore.YELLOW + "This book is already marked as read.")
                back = input(Fore.MAGENTA + "Press Enter to go back to the main menu")
                return
                
            confirm = input(Fore.YELLOW + "Are you sure you want to mark this book as read? (y/n): " + Fore.WHITE)
            if confirm.lower() == "y":
                book['Read Status'] = True
                print(Fore.GREEN + "Book marked as read")
                back = input(Fore.MAGENTA + "Press Enter to go back to the main menu")
                return
            else:
                print(Fore.YELLOW + "Book not marked as read")
                back = input(Fore.MAGENTA + "Press Enter to go back to the main menu")
                return
    print(Fore.RED + "Book not found")
    back = input(Fore.MAGENTA + "Press Enter to go back to the main menu")

def save_books():
    with open('books.json', 'w') as file:
        json.dump(books, file, indent=4)

print("\n" + Fore.CYAN + "=" * 50)
print(Fore.CYAN + Style.BRIGHT + "{:^50}".format("Welcome to the Library Manager"))
print(Fore.CYAN + "=" * 50 + "\n")

running = True
while running:
    print("\n" + Fore.CYAN + "-" * 40)
    print(Fore.CYAN + Style.BRIGHT + "{:^40}".format("MENU OPTIONS"))
    print(Fore.CYAN + "-" * 40)
    print(f"{Fore.CYAN}│ {Fore.YELLOW + Style.BRIGHT}1. {Fore.WHITE}Add a book{Fore.CYAN} {' ' * 21}│")
    print(f"{Fore.CYAN}│ {Fore.YELLOW + Style.BRIGHT}2. {Fore.WHITE}Remove a book{Fore.CYAN} {' ' * 18}│")
    print(f"{Fore.CYAN}│ {Fore.YELLOW + Style.BRIGHT}3. {Fore.WHITE}Search for a book{Fore.CYAN} {' ' * 14}│")
    print(f"{Fore.CYAN}│ {Fore.YELLOW + Style.BRIGHT}4. {Fore.WHITE}Display all books{Fore.CYAN} {' ' * 14}│")
    print(f"{Fore.CYAN}│ {Fore.YELLOW + Style.BRIGHT}5. {Fore.WHITE}Display Statistics{Fore.CYAN} {' ' * 13}│")
    print(f"{Fore.CYAN}│ {Fore.YELLOW + Style.BRIGHT}6. {Fore.WHITE}Mark as read{Fore.CYAN} {' ' * 19}│")
    print(f"{Fore.CYAN}│ {Fore.YELLOW + Style.BRIGHT}7. {Fore.WHITE}Exit{Fore.CYAN} {' ' * 27}│")
    print(Fore.CYAN + "-" * 40)

    try:
        option = int(input(Fore.GREEN + "Enter your choice (1-7): " + Fore.WHITE))

        if option == 1:
            add_book()
        elif option == 2:
            remove_book()
        elif option == 3:
            search_book()
        elif option == 4:
            display_books()
        elif option == 5:
            display_statistics()
        elif option == 6:
            mark_as_read()
        elif option == 7:
            print(Fore.YELLOW + "Saving books...")
            save_books()
            print(Fore.GREEN + "Program Exited")
            running = False
        else:
            print(Fore.RED + "Invalid option. Please enter a number between 1 and 7.")
            back = input(Fore.MAGENTA + "Press Enter to continue")
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a number.")
        back = input(Fore.MAGENTA + "Press Enter to continue")