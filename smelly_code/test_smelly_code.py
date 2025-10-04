"""
Unit Tests for Library Management System
Author: Zain
All tests pass despite the code smells present in the main code.
This demonstrates that smelly code can still be functionally correct.
"""

import unittest
import datetime
import sys
from smelly_code import (
    LibraryManagementSystem, 
    search_books_by_author, 
    search_books_by_category
)


class TestLibraryManagementSystem(unittest.TestCase):
    """
    Comprehensive test suite for the Library Management System.
    Tests all major functionality including book management, member registration,
    checkout processes, fee calculations, and search capabilities.
    """
    
    def setUp(self):
        """
        Set up test fixtures before each test method.
        Creates a fresh instance of LibraryManagementSystem for each test.
        """
        self.library = LibraryManagementSystem()
    
    def test_add_book(self):
        """
        Test that books can be added successfully to the library system.
        Verifies book count, title, and availability tracking.
        """
        self.library.add_book("Test Book", "Test Author", "978-1111111111", "Fiction", 5)
        
        # Verify book was added
        self.assertEqual(len(self.library.books), 1, "Book count should be 1 after adding a book")
        
        # Verify book details
        self.assertEqual(self.library.books[0]['title'], "Test Book", "Book title should match")
        self.assertEqual(self.library.books[0]['author'], "Test Author", "Author name should match")
        self.assertEqual(self.library.books[0]['isbn'], "978-1111111111", "ISBN should match")
        self.assertEqual(self.library.books[0]['available'], 5, "Available copies should be 5")
        self.assertEqual(self.library.books[0]['copies'], 5, "Total copies should be 5")
        
        # Verify category tracking
        self.assertIn("Fiction", self.library.book_categories, "Fiction category should exist")
        self.assertEqual(len(self.library.book_categories["Fiction"]), 1, "Fiction category should have 1 book")
    
    def test_register_member(self):
        """
        Test member registration functionality.
        Verifies member data storage and ID assignment.
        """
        self.library.register_member(
            "John Doe", 
            "john@test.com", 
            "555-1234", 
            "789 Test St", 
            "Regular"
        )
        
        # Verify member was registered
        self.assertEqual(len(self.library.members), 1, "Should have 1 registered member")
        
        # Verify member details
        member = self.library.members[0]
        self.assertEqual(member['name'], "John Doe", "Member name should match")
        self.assertEqual(member['email'], "john@test.com", "Email should match")
        self.assertEqual(member['phone'], "555-1234", "Phone should match")
        self.assertEqual(member['address'], "789 Test St", "Address should match")
        self.assertEqual(member['member_type'], "Regular", "Member type should match")
        self.assertEqual(member['id'], 1, "First member should have ID 1")
        
        # Verify member type tracking
        self.assertIn(1, self.library.member_types, "Member ID should be in member_types")
        self.assertEqual(self.library.member_types[1], "Regular", "Member type should be Regular")
        
        # Verify borrowed books list initialized
        self.assertEqual(len(member['borrowed_books']), 0, "New member should have no borrowed books")
    
    def test_checkout_book_success(self):
        """
        Test successful book checkout process.
        Verifies transaction creation and availability updates.
        """
        # Set up book and member
        self.library.add_book("Checkout Test", "Author X", "978-2222222222", "Science", 2)
        self.library.register_member("Test User", "test@email.com", "555-5678", "321 Test Ave", "Student")
        
        # Perform checkout
        checkout_date = datetime.datetime.now()
        due_date = checkout_date + datetime.timedelta(days=14)
        result = self.library.process_book_checkout(
            1,  # member_id
            "978-2222222222",  # isbn
            checkout_date,
            due_date,
            "Staff A",
            "Desk 1"
        )
        
        # Verify checkout succeeded
        self.assertTrue(result, "Checkout should succeed when book is available")
        
        # Verify transaction created
        self.assertEqual(len(self.library.transactions), 1, "Should have 1 transaction")
        transaction = self.library.transactions[0]
        self.assertEqual(transaction['member_id'], 1, "Transaction member_id should match")
        self.assertEqual(transaction['isbn'], "978-2222222222", "Transaction ISBN should match")
        self.assertFalse(transaction['returned'], "Book should not be marked as returned")
        
        # Verify book availability decreased
        self.assertEqual(self.library.books[0]['available'], 1, "Available copies should decrease to 1")
        
        # Verify member's borrowed books updated
        member = self.library.members[0]
        self.assertIn("978-2222222222", member['borrowed_books'], "ISBN should be in member's borrowed books")
    
    def test_checkout_book_unavailable(self):
        """
        Test checkout fails when book is unavailable.
        Verifies proper error handling for non-existent books.
        """
        # Try to checkout non-existent book
        result = self.library.process_book_checkout(
            1,  # member_id
            "978-9999999999",  # non-existent ISBN
            datetime.datetime.now(), 
            datetime.datetime.now(), 
            "Staff B", 
            "Desk 2"
        )
        
        # Verify checkout failed
        self.assertFalse(result, "Checkout should fail when book doesn't exist")
        
        # Verify no transaction created
        self.assertEqual(len(self.library.transactions), 0, "No transaction should be created for failed checkout")
    
    def test_calculate_overdue_fees(self):
        """
        Test overdue fee calculation for late book returns.
        Verifies fee calculation logic and notification generation.
        """
        # Set up book and member
        self.library.add_book("Fee Test Book", "Author Y", "978-3333333333", "History", 1)
        self.library.register_member("Late User", "late@email.com", "555-9999", "999 Late St", "Regular")
        
        # Create overdue checkout (20 days ago, due 14 days ago means 6 days overdue)
        checkout_date = datetime.datetime.now() - datetime.timedelta(days=20)
        due_date = checkout_date + datetime.timedelta(days=14)
        self.library.process_book_checkout(
            1,  # member_id
            "978-3333333333",  # isbn
            checkout_date,
            due_date,
            "Staff C",
            "Desk 3"
        )
        
        # Calculate fees for return today (6 days overdue)
        return_date = datetime.datetime.now()
        result = self.library.calculate_and_process_overdue_fees_with_notifications_and_updates(
            1,  # member_id
            return_date
        )
        
        # Verify result exists
        self.assertIsNotNone(result, "Fee calculation should return a result")
        
        # Verify fees were calculated
        self.assertGreater(result['total_fee'], 0, "Total fee should be greater than 0 for overdue books")
        
        # Verify overdue books detected
        self.assertEqual(len(result['overdue_books']), 1, "Should have 1 overdue book")
        self.assertGreater(result['overdue_books'][0]['days'], 0, "Days overdue should be positive")
        
        # Verify member_id matches
        self.assertEqual(result['member_id'], 1, "Result should be for member_id 1")
        
        # Verify notifications generated
        self.assertGreater(len(self.library.notifications), 0, "Notifications should be generated")
        
        # Verify overdue fees tracked
        self.assertIn(1, self.library.overdue_fees, "Member should have overdue fees recorded")
        self.assertGreater(self.library.overdue_fees[1], 0, "Overdue fee should be positive")
    
    def test_search_books_by_author(self):
        """
        Test searching books by author name.
        Verifies search functionality and result formatting.
        """
        # Add multiple books by same author
        self.library.add_book("Book 1", "Famous Writer", "978-4444444444", "Drama", 2)
        self.library.add_book("Book 2", "Famous Writer", "978-5555555555", "Drama", 3)
        self.library.add_book("Book 3", "Other Author", "978-6666666666", "Drama", 1)
        
        # Search for Famous Writer
        results = search_books_by_author(self.library, "Famous Writer")
        
        # Verify results
        self.assertIsNotNone(results, "Search should return results")
        self.assertEqual(len(results), 2, "Should find 2 books by Famous Writer")
        
        # Verify result format
        self.assertIn("Book 1", results[0], "First result should contain Book 1")
        self.assertIn("Famous Writer", results[0], "Result should contain author name")
        self.assertIn("978-4444444444", results[0], "Result should contain ISBN")
    
    def test_search_books_by_category(self):
        """
        Test searching books by category.
        Verifies category-based search and filtering.
        """
        # Add books in different categories
        self.library.add_book("Science Book 1", "Scientist A", "978-6666666666", "Science", 1)
        self.library.add_book("Science Book 2", "Scientist B", "978-7777777777", "Science", 2)
        self.library.add_book("Fiction Book", "Novelist", "978-8888888888", "Fiction", 1)
        
        # Search for Science category
        results = search_books_by_category(self.library, "Science")
        
        # Verify results
        self.assertIsNotNone(results, "Search should return results")
        self.assertEqual(len(results), 2, "Should find 2 Science books")
        
        # Verify results contain correct books
        results_text = ' '.join(results)
        self.assertIn("Science Book 1", results_text, "Results should include Science Book 1")
        self.assertIn("Science Book 2", results_text, "Results should include Science Book 2")
        self.assertNotIn("Fiction Book", results_text, "Results should not include Fiction books")
    
    def test_generate_member_report(self):
        """
        Test member report generation functionality.
        Verifies report format and content completeness.
        """
        # Register a member
        self.library.register_member(
            "Report User", 
            "report@email.com", 
            "555-0000", 
            "111 Report Rd", 
            "Premium"
        )
        
        # Generate report
        report = self.library.generate_member_report(1)
        
        # Verify report exists
        self.assertIsNotNone(report, "Report should be generated")
        
        # Verify report contains member information
        self.assertIn("Report User", report, "Report should contain member name")
        self.assertIn("report@email.com", report, "Report should contain email")
        self.assertIn("555-0000", report, "Report should contain phone")
        self.assertIn("111 Report Rd", report, "Report should contain address")
        self.assertIn("Premium", report, "Report should contain member type")
        
        # Verify report structure
        self.assertIn("Member Report for", report, "Report should have proper header")
        self.assertIn("Books Borrowed:", report, "Report should show borrowed books count")


def run_tests_with_summary():
    """
    Run all tests and provide a detailed summary.
    This function is called when the script is run directly.
    """
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestLibraryManagementSystem)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
        print("The Library Management System is working correctly despite code smells.")
    else:
        print("\n❌ SOME TESTS FAILED")
        sys.exit(1)
    
    print("="*70)


if __name__ == '__main__':
    # Run tests with detailed output
    run_tests_with_summary()