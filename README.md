# BookStore

<h1 align="center">Rogalowski's Project <img src="https://komarev.com/ghpvc/?username=rogalowski&label=Profile%20views&color=0e75b6&style=flat" alt="rogalowski" /></h1>

<h3 align="left">Connect with me:</h3>
<p align="left">
<a href="https://linkedin.com/in/jacek-rogowski" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="jacek-rogowski" height="30" width="40" /></a>
<a href="https://instagram.com/jack_jrogow" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="jack_jrogow" height="30" width="40" /></a>
</p>

<h3 align="left">Languages and Tools:</h3>
<p align="left"> <a href="https://babeljs.io/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/babeljs/babeljs-icon.svg" alt="babel" width="40" height="40"/> </a> <a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/> </a> <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-original.svg" alt="django" width="40" height="40"/> </a> <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a> <a href="https://flask.palletsprojects.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg" alt="flask" width="40" height="40"/> </a> <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a> <a href="https://www.linux.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="linux" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://reactjs.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/react/react-original-wordmark.svg" alt="react" width="40" height="40"/> </a> <a href="https://webpack.js.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/d00d0969292a6569d45b06d3f350f463a0107b0d/icons/webpack/webpack-original-wordmark.svg" alt="webpack" width="40" height="40"/> </a> </p>

![](http://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=rogalowski&theme=solarized)

<p>  <img align="center" src="https://github-readme-stats.vercel.app/api?username=rogalowski&show_icons=true&locale=en" alt="rogalowski" /> &nbsp; <img align="left" src="https://github-readme-stats.vercel.app/api/top-langs?username=rogalowski&show_icons=true&locale=en&layout=compact" alt="rogalowski" /> </p>

<h1 align="center">BookStore</h1>

# CONFIGURATION & REQUIREMENTS

asgiref==3.5.2
backports.zoneinfo==0.2.1
distlib==0.3.4
Django==4.0.5
django-extensions==3.1.5
filelock==3.7.1
pbr==5.9.0
pkg_resources==0.0.0
platformdirs==2.5.2
psycopg2==2.9.3
six==1.16.0
sqlparse==0.4.2
stevedore==3.5.0
virtualenv==20.14.1
virtualenv-clone==0.5.7
virtualenvwrapper==4.8.4

# DESCRIPTION

Challenge
Mr Czesław from the STX BookStore company asked you for help with writing an application that will allow him to browse the list of books and help him understand what needs to be ordered for his bookstores.

The application must be a REST API. It needs to allow for some basic operations, such as:
• getting the list of books from the database
• adding a new book
• editing an existing book
• removing the book from the database

When it comes to getting the list of books, Mr Czesław wants to be able to filter the results by title, author, publication year (where the range of years is given) and by the acquired state (if the book is already acquired or not).

Mr Czesław would like to have the option to import books into his database using the publicly available Google API:
• https://developers.google.com/books/docs/v1/using#WorkingVolumes (usage example: https://www.googleapis.com/books/v1/volumes?q=Hobbit )

Mr Czesław wants to be able to import books by a given author via API. In response, he wants to see the number of imported books.

API

    • getting the info about API (“version” string has to be hardcoded to the exact value specified below)

GET /api_spec
Expected response
{
"info": {
"version": "2022.05.16"
}
}

    • getting the list of books from the database

GET /books

GET /books?author="Tolkien"&from=2003&to=2022&acquired=false

    Expected response format:

[
{
"id": 123,
"external_id": "rToaogEACAAJ",
"title": "Hobbit czyli Tam i z powrotem",
"authors": [
"J. R. R. Tolkien"
],
"acquired": false,
"published_year": "2004"
"thumbnail": "http://books.google.com/books/content?id=YyXoAAAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api"
},
{
"id": 340,
"external_id": "EsiJcusIVD",
"title": "A Middle English Reader",
"authors": [
"Kenneth Sisam",
"J. R. R. Tolkien"
],
"acquired": false,
"published_year": "2005",
"thumbnail": null
}
]

    • get details of single book

GET /books/123

Response:
{
"id": 123,
"external_id": "rToaogEACAAJ",
"title": "Hobbit czyli Tam i z powrotem",
"authors": [
"J. R. R. Tolkien"
],
"published_year": "2005",
"acquired": false,
"thumbnail": "http://books.google.com/books/content?id=YyXoAAAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api"
}

    • add a new book to collection

POST /books

Response:
{
"external_id": null,
"title": "Magiczna księga",
"authors": [],
"published_year": "2022",
"acquired": true,
"thumbnail": null
}

Response:
{
"id": 666,
"external_id": null,
"title": "Magiczna księga",
"authors": [],
"published_year": "2022",
"acquired": true,
"thumbnail": null
}

    • update details of single book

PATCH /books/123
Example request body:
{
"acquired": true
}
Example response:
{
"id": 123,
"external_id": "rToaogEACAAJ",
"title": "Hobbit czyli Tam i z powrotem",
"authors": [
"J. R. R. Tolkien"
],
"published_year": "2005",
"acquired": true,
"thumbnail": "http://books.google.com/books/content?id=YyXoAAAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api"
}

    • delete a book

DELETE /books/123

    • import books

Download data about books from https://www.googleapis.com/books/v1/volumes for requested author. Add new entries into the application database. Update already existing ones.
POST /import

Example request body:
{
"author": "nazwisko"
}

Example response with imported book count:
{
"imported": 51
}

Technical requirements
• Implement the application using one of the Python web frameworks (your choice)
• Deploy the application using a publicly available server, for example, Heroku
• Take care of good coding practices (PEP8, code organization, etc.)

When submitting the task, please provide us with:
• URL for the deployed application
• link to the public repository, so that our technical recruiters can look at the code.
