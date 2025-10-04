# Code Smells in Library Management System

**Author:** Zain  
**File:** `smelly_code.py`  
**Total Lines:** 250 LOC

---

## 1. Long Method

**Location:** Lines 99-160  
**Method:** `calculate_and_process_overdue_fees_with_notifications_and_updates()`

**Justification:**  
This method spans 62 lines and performs multiple responsibilities including fee calculation, notification generation, statistics updating, and data storage. It violates the Single Responsibility Principle by doing too much in one place, making it difficult to test and maintain.

---

## 2. God Class (Blob)

**Location:** Lines 15-180  
**Class:** `LibraryManagementSystem`

**Justification:**  
This class has 8 instance attributes and 6 methods handling books, members, transactions, fees, notifications, and reporting. It has too many responsibilities and should be split into separate classes like BookManager, MemberManager, TransactionManager, and NotificationService for better cohesion.

---

## 3. Duplicated Code

**Location 1:** Lines 186-200 (Function: `search_books_by_author`)  
**Location 2:** Lines 204-218 (Function: `search_books_by_category`)

**Justification:**  
Both search functions contain nearly identical logic - they iterate through books, filter by a criterion, check for empty results, and format output identically. This duplication should be extracted into a generic search function with a filter parameter.

---

## 4. Large Parameter List

**Location:** Lines 65-95  
**Method:** `process_book_checkout()`

**Justification:**  
This method takes 6 parameters (member_id, isbn, checkout_date, due_date, staff_name, location), making it cumbersome to call and error-prone. These parameters should be encapsulated in a CheckoutRequest object to improve readability and reduce coupling.

---

## 5. Magic Numbers

**Location:** Lines 119-135  
**Method:** `calculate_and_process_overdue_fees_with_notifications_and_updates()`

**Justification:**  
The fee calculation contains hard-coded values (5, 7, 35, 10, 14, 105, 15, 30, 345, 20) without explanation. These numbers represent business rules for late fees but lack context, making the logic unclear and hard to modify when fee structures change.

---

## 6. Feature Envy

**Location:** Lines 164-180  
**Method:** `generate_member_report()`

**Justification:**  
This method extensively uses member object data (name, email, phone, address, member_type, borrowed_books, registration_date) rather than the LibraryManagementSystem's own data. It demonstrates feature envy by being more interested in the Member's data than its own, suggesting it should belong to a Member class instead.

---

## Testing

All 8 unit tests pass successfully despite these code smells, demonstrating that smelly code can still be functionally correct while remaining difficult to maintain and extend.