CodingSphere
A Simple API with JWT Authentication and RBAC

Code Structure:
API:
main.py
Contains all the logic, API endpoints, and MongoDB connectivity.

model.py
Defines the User and Project models, which are imported into main.py.

requirements.txt
Lists all dependencies that need to be installed.

Instructions to Run:
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Note: Ensure the environment variables are properly set in the .env file.

Open Visual Studio Code or your preferred code editor.

To run the application, use the following steps:

(Optional) Navigate to the API directory if your main.py is located inside the API folder:
bash
Copy code
cd API
Run the application with the following command:
bash
Copy code
uvicorn main:app --reload
