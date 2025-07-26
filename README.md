# Job Portal Application

A comprehensive Django-based job portal web application that connects employers with job seekers. This application allows employers to post jobs and applicants to search and apply for positions.

## 🎯 Assignment Overview

This project fulfills the requirements for Module 26 Assignment: "Build a Job Portal Application with Search Functionality" using Django framework.

## ✨ Features

### User Management
- **Two User Roles**: Employer and Applicant
- **User Registration**: Complete registration system with role selection
- **Authentication**: Secure login/logout functionality
- **Role-based Access**: Different dashboards and permissions for each user type

### Employer Features
- **Job Posting**: Create and publish job listings
- **Job Management**: View all posted jobs
- **Application Management**: View applicants for each job
- **Applicant Review**: Access resumes and cover letters
- **Contact System**: Direct email contact with applicants

### Applicant Features
- **Job Browsing**: View all available job listings
- **Advanced Search**: Search jobs by title, company name, and location
- **Job Application**: Apply with resume upload and cover letter
- **Application Tracking**: View submitted applications
- **Dashboard**: Personalized dashboard with statistics

### Search Functionality
- **Multi-field Search**: Search by job title, company name, or location
- **Real-time Filtering**: Instant search results
- **User-friendly Interface**: Clean search bar with helpful placeholders

### Admin Panel
- **Custom Admin Interface**: Branded admin panel
- **Model Management**: Full CRUD operations for all models
- **Advanced Filtering**: Filter jobs by date, location, and company
- **Search Capabilities**: Search across all relevant fields
- **Statistics**: View application counts and user data

## 🏗️ Technical Architecture

### Models

#### UserProfile
- Extends Django's built-in User model
- Stores user role (employer/applicant)
- Links to User with OneToOne relationship

#### Job
- **title**: Job position title
- **company_name**: Company offering the job
- **location**: Job location
- **description**: Detailed job description
- **posted_by**: Foreign key to User (employer)
- **created_at**: Timestamp of job creation

#### Application
- **job**: Foreign key to Job
- **applicant**: Foreign key to User
- **resume**: File upload field for resume
- **cover_letter**: Text field for cover letter
- **applied_at**: Timestamp of application

### Views Architecture
- **Class-based Views**: Utilizing Django's CBVs for better organization
- **Function-based Views**: For complex business logic
- **Authentication Decorators**: Ensuring proper access control
- **Role-based Redirects**: Automatic redirection based on user role

### Template System
- **Base Template**: Consistent layout across all pages
- **Responsive Design**: Mobile-friendly Bootstrap implementation
- **Dynamic Navigation**: Role-based navigation menus
- **Interactive Elements**: Modern UI with JavaScript enhancements

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Django 4.0+
- Pillow (for image handling)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd job_portal
   ```

2. **Install Dependencies**
   ```bash
   pip install django pillow
   ```

3. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**
   - Main Application: http://localhost:8000/
   - Admin Panel: http://localhost:8000/admin/

## 📱 User Guide

### For Applicants

1. **Registration**
   - Visit the registration page
   - Fill in personal details
   - Select "Applicant" as role
   - Create account

2. **Job Search**
   - Browse all jobs from the dashboard
   - Use search functionality to filter jobs
   - View detailed job descriptions

3. **Applying for Jobs**
   - Click on job listings
   - Upload resume (PDF/DOC format)
   - Write cover letter
   - Submit application

4. **Track Applications**
   - View all submitted applications
   - Check application status
   - Access application history

### For Employers

1. **Registration**
   - Register with "Employer" role
   - Access employer dashboard

2. **Post Jobs**
   - Navigate to "Post Job"
   - Fill in job details
   - Publish job listing

3. **Manage Applications**
   - View all posted jobs
   - Check applicants for each job
   - Download resumes
   - Contact applicants directly

### For Administrators

1. **Access Admin Panel**
   - Login with superuser credentials
   - Navigate to /admin/

2. **Manage Data**
   - View all users, jobs, and applications
   - Use filtering and search features
   - Perform bulk operations

## 🔧 Configuration

### Settings Configuration
- **Database**: SQLite (default) - easily configurable for PostgreSQL/MySQL
- **Media Files**: Configured for file uploads
- **Static Files**: Bootstrap and custom CSS/JS
- **Security**: CSRF protection and secure authentication

### URL Configuration
- Clean URL patterns
- Namespace organization
- RESTful routing

## 🎨 Frontend Design

### Technologies Used
- **Bootstrap 5**: Responsive framework
- **Font Awesome**: Icon library
- **Custom CSS**: Enhanced styling
- **JavaScript**: Interactive elements

### Design Features
- **Responsive Layout**: Works on all device sizes
- **Modern UI**: Clean and professional design
- **Intuitive Navigation**: Easy-to-use interface
- **Visual Feedback**: Success/error messages
- **Loading States**: User-friendly interactions

## 🔒 Security Features

- **Authentication Required**: Protected views
- **Role-based Access**: Proper permission checks
- **CSRF Protection**: Secure form submissions
- **File Upload Security**: Validated file types
- **SQL Injection Protection**: Django ORM usage

## 📊 Database Schema

```
User (Django built-in)
├── UserProfile (1:1)
│   └── role (employer/applicant)
│
Job
├── posted_by (FK to User)
└── Applications (1:Many)
    ├── job (FK to Job)
    ├── applicant (FK to User)
    ├── resume (FileField)
    └── cover_letter (TextField)
```

## 🧪 Testing

The application has been thoroughly tested for:
- User registration and authentication
- Role-based access control
- Job posting and management
- Application submission and tracking
- Search functionality
- Admin panel operations
- File upload handling
- Responsive design

## 📈 Future Enhancements

Potential improvements for future versions:
- Email notifications for new applications
- Advanced filtering options
- Job recommendation system
- Company profiles
- Application status tracking
- Interview scheduling
- Payment integration for premium features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

**Note**: This application is designed for educational purposes and demonstrates Django best practices for building a complete web application with user authentication, file handling, and database relationships.

