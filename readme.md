<a name="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

* A microservice API to help understand and track how a particular person’s flight path may be queried.
* The API should accept a request that includes a list of flights defined by a source and destination airport code.
* These flights may not be listed in order and must be sorted to find the total flight paths starting and ending at airports.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- BUILT WITH -->
### Built With

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/3.0.x/#)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Layout
https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/

### Run application
flask --app flaskr/__init__.py run

### Docs
http://127.0.0.1:8080/apidocs/

### Test application
python -m pytest

<p align="right">(<a href="#readme-top">back to top</a>)</p>