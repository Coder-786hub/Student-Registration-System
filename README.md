# Student Registration System

This is a GUI-based Student Registration System built using Python's Tkinter library. The system allows users to register students, upload their images, and store their details in a MySQL database. The application also provides functionality to search, update, and reset student records.

## Features

- Register new students
- Upload student images
- Save student details to a MySQL database
- Search for students by registration number
- Update student records
- Reset form fields
- Simple and intuitive user interface

## Prerequisites

- Python 3.x
- MySQL server
- Required Python libraries: `tkinter`, `PIL` (Pillow), `mysql-connector-python`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/student-registration-system.git
    ```

2. Navigate to the project directory:
    ```sh
    cd student-registration-system
    ```

3. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the MySQL database:
    - Create a database named `PROJECT`.
    - Create a table named `admin` with the following schema:
      ```sql
      CREATE TABLE admin (
          registration_no INT PRIMARY KEY,
          name VARCHAR(255),
          dob DATE,
          gender VARCHAR(10),
          class VARCHAR(50),
          religion VARCHAR(50),
          skill VARCHAR(255),
          father_name VARCHAR(255),
          mother_name VARCHAR(255),
          father_occupation VARCHAR(255),
          mother_occupation VARCHAR(255)
      );
      ```

5. Update the database connection details in the script:
    ```python
    connection = mysql.connector.connect(
        host="localhost",
        database="PROJECT",
        user="your_mysql_username",
        password="your_mysql_password"
    )
    ```

## Usage

1. Run the application:
    ```sh
    python app.py
    ```

2. The main window of the application will appear.

3. Fill in the student details and upload the student's image.

4. Click the `Save` button to save the student details in the database.

5. Use the `Search` feature to find a student by their registration number.

6. Use the `Update` button to modify existing student records.

7. Use the `Reset` button to clear the form fields.

8. Click `Exit` to close the application.

## Screenshots

![Main Window](screenshots/main_window.png)

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or suggestions, feel free to contact me at [aftablamkhan8391y@gmail.com](mailto:aftablamkhan8391@gmail.com).(Contact me : +91 9721839101).
