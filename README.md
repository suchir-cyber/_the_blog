# BlogWeb

A Django-based web application for creating, viewing, and managing blogs. Users can perform CRUD (Create, Read, Update, Delete) operations on their own blogs, search and filter posts, and enjoy additional features like authentication, pagination, and a contact page.

---

## **Features**

### **Blog Management**
- **CRUD Operations**: 
  - Users can create, update, and delete their own blogs.
  - Other users can only view blogs but not modify them.
- **Pagination**:
  - Blog posts are paginated to limit the number of posts displayed per page.
- **Search Functionality**:
  - Users can search for blogs using a search bar, based on blog titles or descriptions.
- **Date Filtering**:
  - Users can filter posts by specifying a start date and end date.

### **User Authentication**
- Secure user authentication and authorization features:
  - Registration and login functionality.
  - Password recovery using the "Forgot Password" feature via an SMTP email server.

### **Contact Page**
- A contact form where users can send messages directly to the admin using the SMTP server.

---
## **ScreenShots**
1.Home Page

   ![Screenshot 2024-12-18 001700](https://github.com/user-attachments/assets/b58650b4-3134-489c-a791-f184e72c1ed0)

2.Create Blog

   ![Screenshot 2024-12-18 004344](https://github.com/user-attachments/assets/c55008db-bb00-43af-8614-9425b8fceb3f)

3.Filter Blogs
  
  ![Screenshot 2024-12-18 004440](https://github.com/user-attachments/assets/a01c961d-a4f5-4feb-95d9-bd637e21b93b)

4.Contact Page

  ![Screenshot 2024-12-18 004542](https://github.com/user-attachments/assets/fc6466c2-9adc-4a8c-b2d6-04cce154cf10)

## **Demo Video**
 
  https://github.com/user-attachments/assets/1e1ef10d-aaa4-4201-84af-38ee6dee1a1a

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/blog-app.git
   cd blog-app
   ```

2. Create a virtual environment and activate it:
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

 3. Install dependencies:
    ```bash
       pip install -r requirements.txt
    ```
 4. Set up the database:
    ```bash
        python manage.py makemigrations
        python manage.py migrate
     ```   

 5. Run the development server:
    ```bash
      python manage.py runserver
    ```
  
Access the application at http://127.0.0.1:8000/.

## Usage

### **Creating and Managing Blogs**
- Sign in to your account.
- Navigate to the blog section.
- Perform the following operations:
  - **Create**: Add a new blog post.
  - **Update**: Edit your existing blog posts.
  - **Delete**: Remove your own blog posts.

### **Viewing Other Users' Blogs**
- View blogs created by other users but without edit or delete permissions.

### **Searching and Filtering Blogs**
- Use the search bar to find blogs by title or description.
- Use the start date and end date fields to filter blogs by date.

### **Password Recovery**
- If you forget your password, use the "Forgot Password" feature to reset it. 
- An email with reset instructions will be sent to your registered email address.

### **Contact Page**
- Navigate to the contact page to send a message or query directly to the admin via email.

## Technologies Used

- **Backend**: Django (Python)
- **Database**: SQLite (default) or any preferred database (e.g., PostgreSQL, MySQL)
- **Frontend**: Django templates, HTML, CSS
- **Authentication**: Django's built-in authentication system
- **Email**: SMTP server for sending emails

## Setup for SMTP Email

1. Add your SMTP credentials in `settings.py`:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = '<your-email@example.com>'
   EMAIL_HOST_PASSWORD = '<your-email-password>'
   ```
 2. Ensure less secure apps or app-specific passwords are enabled for your email account.

    Note: Using app-specific passwords is recommended for better security.  


## Future Enhancements

- Add user profile pages.
- Enable category-based filtering for blogs.
- Implement notifications for new blog posts.
