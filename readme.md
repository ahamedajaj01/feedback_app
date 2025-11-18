📝 Feedback Application — Django Project

A simple, clean, beginner-friendly Django web application where users can register, log in, submit feedback, view their own feedback, and admins can manage all feedback.

This app demonstrates user authentication, role-based access, CRUD operations, and clean Bootstrap UI.

🚀 Features
👤 User Features

Register with username, email, password

Login / Logout

Submit Feedback

Name

Email

Message

View My Feedback

Each user can only see feedback submitted by themselves

Edit My Feedback

Delete My Feedback

Friendly UI using Bootstrap

🔐 Admin Features

Admin login (Django admin panel)

Admin/staff automatically redirected to Feedback List Page (not homepage)

View all user feedback in admin dashboard page

Admin cannot access user pages like My Feedback

User cannot access admin pages

🏗 Technology Stack

Python 5.3

Django (Authentication, ORM, Views)

MySQL database

Bootstrap 5 (UI styling)


📌 Key Functional Logic
🗄 Feedback Model
Stores:

Name

Email

Message

Created Time

User who submitted

📝 Feedback Submission
Normal users can submit feedback

Form validates message

After submit, user stays on same page with success message

👀 My Feedback Page
Shows feedback only from logged-in user

Edit + Delete buttons available

Protected: admin cannot access

🛠 Edit Feedback
User can only edit their own feedback

Edit form pre-fills existing values

Basic security checks ensure ownership

❌ Delete Feedback
POST-based delete

Only owner can delete

Confirmation optional

🔒 Authentication & Routing
Registration: free for all

Login: redirects based on role

Admin visiting homepage → redirected to admin feedback list

Normal user visiting admin URL → blocked/redirected

Login/Register pages hidden for logged-in users

🔧 Installation & Setup
1. Clone the project
git clone <your-repo-url>
cd project

2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3. Install dependencies
pip install django

4. Migrate database
python manage.py migrate

5. Create superuser (admin)
python manage.py createsuperuser

6. Run the server
python manage.py runserver

7. Access the app

Website → http://127.0.0.1:8000/

Admin panel → http://127.0.0.1:8000/admin/

🖼 UI Highlights

Clean Bootstrap layout

Centered login / register cards

Alert messages with closable (X) button

Neatly formatted feedback cards

Edit/Delete buttons right aligned

✔ Future Enhancements (optional)

Add pagination to admin feedback list

Add search/filter system for admin

Add email notifications for new feedback

Switch to Django class-based views

Add profile page for users