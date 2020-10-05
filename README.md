# sample-data-generator
A UI to generate sample data for the Quarantine Help app.

## Steps for local development

1. Install pyenv and its virtualenv manager using

   ```
   $ brew install pyenv
   $ brew install pyenv-virtualenv
   $ pyenv install 3.7.5
   $ eval "$(pyenv init -)"
   sample-data-generator/$ pyenv virtualenv 3.7.5 env-3.7.5
   ```

   This will create a pyenv-virtualenv for you and probably place it on your
   `~/home/<username>/.pyenv/versions/`. You can activate that manually using

   ```
   sample-data-generator/$ source ~/.pyenv/versions/env-3.7.5/bin/activate
   ```

   or even better:

   ```
   sample-data-generator/$ pyenv activate env-3.7.5
   ```

   or, there are better ways to do this if you follow [Pyenv:Docs](https://github.com/pyenv/pyenv-virtualenv)

2. Now you are in the right environment, install dependencies using:
   ```
   (env-3.7.5) sample-data-generator/$ pip install -r requirements.txt
   ```
3. Install `postgis` using `brew install postgis`. You can create a database and set the user roles using the following commands:
   ```
   CREATE DATABASE data_gen_db;
   CREATE USER data_gen_user WITH PASSWORD 'ABCD123<changeThis>';
   GRANT ALL PRIVILEGES ON DATABASE data_gen_db TO data_gen_user;
   ALTER ROLE data_gen_user SET timezone TO 'UTC';
   ALTER ROLE data_gen_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE data_gen_user SET client_encoding TO 'utf8';
   ```
4. We use `pre-commit` hooks to format code. See that you install it using
   https://pre-commit.com/. Later, install our pre-commit hooks using
   ```
   (env-3.7.5) sample-data-generator/$ pre-commit install
   ```
5. There are some `local_settings` you need to have as part of running the
   server. You can copy a template using:
   ```
   (env-3.7.5) sample-data-generator/$ cp sample_data_generator/local_settings_sample.py sample_data_generator/local_settings.py
   ```
   You need to modify the values there to use the applicaiton in full.
6. Run the Django standard runserver steps:
   ```
   (env-3.7.5) sample-data-generator/$ python manage.py migrate
   (env-3.7.5) sample-data-generator/$ python manage.py collectstatic
   (env-3.7.5) sample-data-generator/$ python manage.py runserver
   ```
   or even better, run it from pyCharm using your debugger.
7. Create a superuser and add some initial data to the database.

```
(env-3.7.5) sample-data-generator/$ python manage.py createsuperuser
```

Now you have the app locally running! 
