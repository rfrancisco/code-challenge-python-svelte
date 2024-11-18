#**************************************************
# clean up the project
#**************************************************
rm -rf **/.venv
rm -rf **/__pycache__
rm -rf **/instance
rm -rf **/node_modules
rm -rf **/node_modules
rm -rf **/dist

#**************************************************
# initialize the backend
#**************************************************
(
    cd backend;
    # create a python virtual environment
    python3 -m venv .venv
    # activate the virtual environment
    source .venv/bin/activate
    # install dependencies
    pip3 install -r requirements.txt
    # create and initialize the database
    python3 init.py
)
#**************************************************
# initialize the frontend
#**************************************************
(
    cd frontend;
    # install dependencies
    npm install
)