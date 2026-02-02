\# AI Business English Sentence Optimizer



A Streamlit web app that rewrites business English text. Includes input validation and pytest tests.



\## Features

\- Two modes: Correct + 3 paragraphs / Rewrite (1 paragraph)

\- Input validation (length, allowed characters, repeated words)

\- Calls OpenAI API and displays the result

\- Automated tests for validation



\## Run locally

1\) Set your API key (Windows PowerShell):

```powershell

setx OPENAI\_API\_KEY "YOUR\_KEY"





md

\## Project structure

app/

&nbsp; streamlit\_app.py

&nbsp; validation.py

&nbsp; prompting.py

&nbsp; client.py

tests/

&nbsp; test\_validation.py



