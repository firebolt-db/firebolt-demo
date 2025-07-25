# Firebolt ❤️ Streamlit

This is a demo data app built with Firebolt and Streamlit. It uses the AdTech dataset (57B rows).

To get started, you need Python >= 3.7, Firebolt Python SDK and Streamlit.

First step, install the depedencies:

```bash
pip install -r requirements.txt
```

Update the secrets.toml file in the .streamlit folder.

This file contains your Firebolt username/password. If using Firebolt 2.0, service account credentials are required Here is a sample:

```
"db_username" = "my_firebolt_username"
"db_password" = "my_firebolt_password"
```

Update the connection section in streamlit_app.py file:
```
connection = connect(
        engine_name="ENGINE_NAME",
        database="DB_NAME",
        account_name="ACCOUNT_NAME",
        auth=ClientCredentials(username, password)
    )
``` 


After that, just run your app:

```bash
streamlit run streamlit_app.py
```

The app will now be available on `localhost:8501`.

Authentication should be configured with proper credentials.

# Screenshot:

![image](https://user-images.githubusercontent.com/62242783/199934443-1da074f2-dea6-4c93-8d65-5941a8b4f725.png)
