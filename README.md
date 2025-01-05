# CodingSphere: A Simple API with JWT Authentication and RBAC

## Project Structure

- **main.py**: Contains the logic for API endpoints and MongoDB connectivity.
- **model.py**: Defines the `User` and `Project` models, which are imported into `main.py`.
- **requirements.txt**: Lists all the dependencies required for the project.
- **.env** : All Environment Variable included here

## Instructions to Run

### 1. Install Required Dependencies

To install all the necessary Python packages, run the following command:
```bash
pip install -r requirements.txt


2. Set Up Environment Variables
Ensure the environment variables are properly set in the .env file. This is crucial for the correct functioning of the application, as it reads the values from the environment (such as database connection strings, JWT secret keys, etc.).


## Open Visual Studio Code or your preferred code editor.
To run the application, use the following steps:
(Optional) Navigate to the API directory if your main.py is located inside the API folder:
cd API
# Run the application with the following command:
uvicorn main:app --reload




## I could have done deployed the fastapi on Lambda but As there is An issues with my AWS account so I haven't deployed.
