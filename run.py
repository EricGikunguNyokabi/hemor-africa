# run.py
from app import create_app

app = create_app()
application = app

if __name__ == "__main__":
    app.run(debug=True)

# python3 run.py