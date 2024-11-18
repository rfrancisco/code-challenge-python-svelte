# Code Challenge

Code challenge application consisting on an application that allow registered users to register their expenses.
The backend is Python using 'Flask', and the frontent is built with 'Svelte'.

## Dependencies

To run and debug this application you will need to have:

*Required*

* Python 3
* Node.js (v22 or above)

*Optional*

* If you use vscode it's recommended to install the official Python and Svelte extensions

## How to run

Prepare backend and frontend:

```sh
# performs necessary initialization
$ sh ./init.sh
```

Start backend at [http://localhost:5000/](http://localhost:5000/):

```sh
$ cd backend
# start the backend
$ python3 src/app.py
```

Backend runs 

Start frontend at [http://localhost:5173/](http://localhost:5173/):

```sh
$ cd frontend
# start the frontend
$ npm run dev
```