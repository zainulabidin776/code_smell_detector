"""
Library Management System - Deliberately Smelly Code
Author: Zain
This code intentionally contains 6 code smells for educational purposes.
"""

import datetime
import random


class LibraryManagementSystem:
    """
    God Class Smell: This class has too many responsibilities.
    It handles books, members, transactions, reporting, and notifications.
    Lines: 15-180
    """
    
    def __init__(self):
        self.books = []
        self.members = []
        self.transactions = []
        self.overdue_fees = {}
        self.book_categories = {}
        self.member_types = {}
        self.notifications = []
        self.system_stats = {}
        
    def add_book(self, title, author, isbn, category, copies):
        """Add a new book to the library"""
        book = {
            'title': title,
            'author': author,
            'isbn': isbn,
            'category': category,
            'copies': copies,
            'available': copies
        }
        self.books.append(book)
        if category not in self.book_categories:
            self.book_categories[category] = []
        self.book_categories[category].append(book)
    
    def register_member(self, name, email, phone, address, member_type):
        """Register a new member"""
        member = {
            'id': len(self.members) + 1,
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'member_type': member_type,
            'borrowed_books': [],
            'registration_date': datetime.datetime.now()
        }
        self.members.append(member)
        self.member_types[member['id']] = member_type
    
    def process_book_checkout(self, member_id, isbn, checkout_date, due_date, staff_name, location):
        """
        Large Parameter List Smell: This method takes too many parameters (6).
        Lines: 65-95
        """
        book = None
        for b in self.books:
            if b['isbn'] == isbn and b['available'] > 0:
                book = b
                break
        
        if not book:
            return False
        
        member = None
        for m in self.members:
            if m['id'] == member_id:
                member = m
                break
        
        if not member:
            return False
        
        book['available'] -= 1
        transaction = {
            'member_id': member_id,
            'isbn': isbn,
            'checkout_date': checkout_date,
            'due_date': due_date,
            'staff_name': staff_name,
            'location': location,
            'returned': False
        }
        self.transactions.append(transaction)
        member['borrowed_books'].append(isbn)
        return True
    
    def calculate_and_process_overdue_fees_with_notifications_and_updates(self, member_id, return_date):
        """
        Long Method Smell: This method is too long (>50 lines) and does too much.
        Lines: 99-160
        """
        member = None
        for m in self.members:
            if m['id'] == member_id:
                member = m
                break
        
        if not member:
            return None
        
        total_fee = 0
        overdue_books = []
        
        for transaction in self.transactions:
            if transaction['member_id'] == member_id and not transaction['returned']:
                days_overdue = (return_date - transaction['due_date']).days
                
                if days_overdue > 0:
                    # Magic Numbers Smell: Hard-coded values without explanation
                    # Lines: 119-135
                    if days_overdue <= 7:
                        fee = days_overdue * 5
                    elif days_overdue <= 14:
                        fee = 35 + (days_overdue - 7) * 10
                    elif days_overdue <= 30:
                        fee = 105 + (days_overdue - 14) * 15
                    else:
                        fee = 345 + (days_overdue - 30) * 20
                    
                    total_fee += fee
                    overdue_books.append({
                        'isbn': transaction['isbn'],
                        'days': days_overdue,
                        'fee': fee
                    })
                    
                    if member_id not in self.overdue_fees:
                        self.overdue_fees[member_id] = 0
                    self.overdue_fees[member_id] += fee
                    
                    notification = f"Member {member['name']} has overdue book {transaction['isbn']} - Fee: ${fee}"
                    self.notifications.append(notification)
                    
                    if days_overdue > 30:
                        urgent_notification = f"URGENT: Member {member['name']} is {days_overdue} days overdue!"
                        self.notifications.append(urgent_notification)
        
        if 'overdue_count' not in self.system_stats:
            self.system_stats['overdue_count'] = 0
        self.system_stats['overdue_count'] += len(overdue_books)
        
        return {
            'member_id': member_id,
            'total_fee': total_fee,
            'overdue_books': overdue_books,
            'notifications_sent': len([n for n in self.notifications if str(member_id) in n])
        }
    
    def generate_member_report(self, member_id):
        """
        Feature Envy Smell: This method uses member data more than its own class data.
        Lines: 164-180
        """
        member = None
        for m in self.members:
            if m['id'] == member_id:
                member = m
                break
        
        if not member:
            return None
        
        report = f"Member Report for {member['name']}\n"
        report += f"Email: {member['email']}\n"
        report += f"Phone: {member['phone']}\n"
        report += f"Address: {member['address']}\n"
        report += f"Member Type: {member['member_type']}\n"
        report += f"Books Borrowed: {len(member['borrowed_books'])}\n"
        report += f"Registration Date: {member['registration_date']}\n"
        
        return report


def search_books_by_author(library, author_name):
    """
    Duplicated Code Smell: Similar logic appears in multiple places.
    Lines: 186-200
    """
    results = []
    for book in library.books:
        if book['author'].lower() == author_name.lower():
            results.append(book)
    
    if len(results) == 0:
        return None
    
    formatted_results = []
    for book in results:
        formatted_results.append(f"{book['title']} by {book['author']} (ISBN: {book['isbn']})")
    
    return formatted_results


def search_books_by_category(library, category_name):
    """
    Duplicated Code Smell: Nearly identical to search_books_by_author.
    Lines: 204-218
    """
    results = []
    for book in library.books:
        if book['category'].lower() == category_name.lower():
            results.append(book)
    
    if len(results) == 0:
        return None
    
    formatted_results = []
    for book in results:
        formatted_results.append(f"{book['title']} by {book['author']} (ISBN: {book['isbn']})")
    
    return formatted_results


def main():
    """Main function to demonstrate the library system"""
    library = LibraryManagementSystem()
    
    # Add some books
    library.add_book("Python Programming", "John Smith", "978-1234567890", "Programming", 3)
    library.add_book("Data Structures", "Jane Doe", "978-0987654321", "Computer Science", 2)
    
    # Register members
    library.register_member("Alice Johnson", "alice@email.com", "555-0101", "123 Main St", "Student")
    library.register_member("Bob Williams", "bob@email.com", "555-0102", "456 Oak Ave", "Faculty")
    
    # Checkout book
    checkout_date = datetime.datetime.now()
    due_date = checkout_date + datetime.timedelta(days=14)
    library.process_book_checkout(1, "978-1234567890", checkout_date, due_date, "Librarian A", "Main Desk")
    
    print("Library Management System Running...")
    print(f"Total Books: {len(library.books)}")
    print(f"Total Members: {len(library.members)}")
    print(f"Total Transactions: {len(library.transactions)}")


if __name__ == "__main__":
    main()