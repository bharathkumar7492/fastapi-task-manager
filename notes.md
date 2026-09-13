
<!-- move SECRET_KEY to .env -->

1). install python-dotenv:
    run: venv\Scripts\python.exe -m pip install python-dotenv
    
Now we'll move your sensitive/configuration values out of Python code.like
# DATABASE_URL=mysql+pymysql://USERNAME:PASSWORD@localhost/task_manager

-# Secret key used to sign and verify the JWT
# SECRET_KEY=your-secret-key
-# Algorithm used to sign the JWT
# ALGORITHM=HS256
-# JWT will expire after 30 minutes
# ACCESS_TOKEN_EXPIRE_MINUTES=30


2). Connect .env to Python Now we'll make Python actually read those values.
# from dotenv import load_dotenv
# import os

# load_dotenv()

instead of hard code, we use : DATABASE_URL = os.getenv("DATABASE_URL")
ex: check in database.py & oauth2.py

---------------------------------------------------------------------------------------

- why we don't upload venv/, but we do upload requirements.txt.

- When someone clones your GitHub project

- They won't have your venv/. But they can create their own:  `python -m venv venv`

- Then install exactly the packages your project needs:
`pip install -r requirements.txt`

- to add your project packages to requirement.txt file 
run: `venv\Scripts\python.exe -m pip freeze > requirements.txt`
