
# Image Classification Web App

This project is a Flask-based web application for image classification. It allows users to upload images and classify them using pre-trained models.

 Setup Instructions (for VM users)

# Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git

# Step 1: Clone the Repository

bash
git clone <repository-url>
cd <project-directory>


# Step 2: Set Up a Virtual Environment

bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate


# Step 3: Install Dependencies

bash
pip install -r requirements.txt


# Step 4: Set Up Environment Variables

Create a .env file in the project root directory and add the following:


FLASK_APP=app
FLASK_ENV=development


# Step 5: Initialize the Database

bash
flask db init
flask db migrate
flask db upgrade


# Step 6: Run the Application

bash
flask run


The application should now be running on http://127.0.0.1:5000/.

 Project Structure

- app/: Main application directory
  - templates/: HTML templates
  - static/: CSS and JavaScript files
  - models/: Database models
  - routes/: Application routes
- instance/: Instance-specific files (e.g., database)
- migrations/: Database migration files
- uploads/: Directory for uploaded images (created automatically)

 Usage

1. Open a web browser and navigate to http://127.0.0.1:5000/.
2. Upload an image using the provided form.
3. Select a classification model from the dropdown menu.
4. Click "Classify" to process the image.
5. View the classification results on the next page.
6. Access the classification history by clicking the "History" link.

 Important Notes

- Ensure that your VM has sufficient memory and processing power to run the image classification models.
- The uploads/ directory is used to store uploaded images temporarily. It's gitignored by default.
- The SQLite database file (*.db) is also gitignored. You may need to back it up separately if you want to preserve classification history.

 Troubleshooting

- If you encounter any issues with file permissions, ensure that your VM user has the necessary rights to read, write, and execute files in the project directory.
- For any port conflicts, you can change the port by running flask run -p <port-number>.



This README provides a comprehensive guide for setting up and running the project in a VM environment. It covers all the necessary steps, from cloning the repository to running the application, and includes important notes about file storage and potential VM-specific considerations.
