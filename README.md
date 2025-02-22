# CodingSphere: A Simple API with JWT Authentication and RBAC

## Project Structure

- **main.py**: Contains the logic for API endpoints and MongoDB connectivity.
- **model.py**: Defines the `User` and `Project` models, which are imported into `main.py`.
- **requirements.txt**: Lists all the dependencies required for the project.
- **.env** : All Environment Variables are included here
- **role**: role should be only user or admin (please only put small not capital)
## Note
## username max_length is 10 so always put less than equal to 10 otherwise you will get Internal Server Error
## Description max_length is 500

## I could have done deployed the fastapi on Lambda but As there is An issues with my AWS account so I haven't deployed.(Also it was optional)
### See the Live Projects (Deployed on render)
# base URL

https://codingsphere-7.onrender.com/
## Go to docs for fastapi
https://codingsphere-7.onrender.com/docs
## for testing first register and then login while Click on Authorize Button which is on top right  now you are ready to use all features mentioned in the assignment. For reference see the below image

![Authorization](./ss.png)
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





