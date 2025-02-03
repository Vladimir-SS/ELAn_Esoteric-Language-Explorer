<!-- Tags: #project #infoiasi #wade #web -->
<div align="center">

  <h1>ELAn-Esoteric-Language-Explorer</h1>

<!-- Badges -->
<p>
  <a href="https://github.com/Vladimir-SS/ELAn_Esoteric-Language-Explorer/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/Vladimir-SS/ELAn_Esoteric-Language-Explorer" alt="contributors" />
  </a>
  <a href="">
    <img src="https://img.shields.io/github/last-commit/Vladimir-SS/ELAn_Esoteric-Language-Explorer" alt="last update" />
  </a>
  <a href="https://github.com/Vladimir-SS/ELAn_Esoteric-Language-Explorer/network/members">
    <img src="https://img.shields.io/github/forks/Vladimir-SS/ELAn_Esoteric-Language-Explorer" alt="forks" />
  </a>
  <a href="https://github.com/Vladimir-SS/ELAn_Esoteric-Language-Explorer/stargazers">
    <img src="https://img.shields.io/github/stars/Vladimir-SS/ELAn_Esoteric-Language-Explorer" alt="stars" />
  </a>
  <a href="https://github.com/Vladimir-SS/ELAn_Esoteric-Language-Explorer/issues/">
    <img src="https://img.shields.io/github/issues/Vladimir-SS/ELAn_Esoteric-Language-Explorer" alt="open issues" />
  </a>
  <a href="https://github.com/Vladimir-SS/ELAn_Esoteric-Language-Explorer/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/Vladimir-SS/ELAn_Esoteric-Language-Explorer.svg" alt="license" />
  </a>
</p>

<h4>
    <a href="https://www.youtube.com/watch?v=oxjl7SNVwlQ">View Demo</a>
  <span> · </span>
    <a href="https://vladimir-ss.github.io/ELAn_Esoteric-Language-Explorer/">Documentation</a>
  <span> · </span>
    <a href="https://github.com/Vladimir-SS/ELAn_Esoteric-Language-Explorer/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/Vladimir-SS/ELAn_Esoteric-Language-Explorer/issues/">Request Feature</a>
  </h4>
</div>

<br />

<!-- Table of Contents -->
# :notebook_with_decorative_cover: Table of Contents

- [:notebook\_with\_decorative\_cover: Table of Contents](#notebook_with_decorative_cover-table-of-contents)
  - [:star2: About the Project](#star2-about-the-project)
    - [:space\_invader: Tech Stack](#space_invader-tech-stack)
  - [:toolbox: Getting Started](#toolbox-getting-started)
    - [:bangbang: Prerequisites](#bangbang-prerequisites)
    - [:gear: Installation](#gear-installation)
    - [:running: Run Locally](#running-run-locally)
  - [:wave: Contributing](#wave-contributing)
  - [:warning: License](#warning-license)



<!-- About the Project -->
## :star2: About the Project


<!-- Screenshots -->
<!-- ### :camera: Screenshots

<div align="center">
  <img src="https://placehold.co/600x400?text=Your+Screenshot+here" alt="screenshot" />
</div> -->


<!-- TechStack -->
### :space_invader: Tech Stack

<details>
  <summary>Client</summary>
  <ul>
    <li><a href="https://www.typescriptlang.org/">Typescript</a></li>
    <li><a href="https://reactjs.org/">React.js</a></li>
    <li><a href="https://vitejs.dev/">Vite</a></li>
  </ul>
</details>

<details>
  <summary>Server</summary>
  <ul>
    <li><a href="https://fastapi.tiangolo.com/">FastAPI</a></li>
  </ul>
</details>

<details>
<summary>Database</summary>
  <ul>
    <li><a href="https://jena.apache.org/documentation/fuseki2/">Apache Jena Fuseki</a></li>
  </ul>
</details>

<details>
<summary>DevOps</summary>
  <ul>
    <li><a href="https://www.docker.com/">Docker</a></li>
  </ul>
</details>

<!-- Getting Started -->
## 	:toolbox: Getting Started

<!-- Prerequisites -->
### :bangbang: Prerequisites

<!-- Installation -->
### :gear: Installation

Install the necessary tools for the project:

1. [Node.js](https://nodejs.org/) (required)
2. [Python](https://www.python.org/) (required)
3. [Apache Jena Fuseki](https://jena.apache.org/download/) (required)
4. [Docker](https://www.docker.com/) (optional)

<!-- Running Tests -->
<!-- ### :test_tube: Running Tests

To run tests, run the following command

```bash
  yarn test test
``` -->

<!-- Run Locally -->
### :running: Run Locally

Clone the project

```bash
git clone https://github.com/Vladimir-SS/ELAn_Esoteric-Language-Explorer.git
```

Go to the project directory

```bash
cd ELAn_Esoteric-Language-Explorer
```

Install dependencies

```bash
# Install frontend dependencies
cd frontend/ ; npm install ; cd ..

# Install backend dependencies (the third command fixes the error with packages not being found)
cd backend/ ; pip install -r requirements.txt ; pip install -e . ; cd ..
```

Start the application

```bash
# Start the frontend
cd frontend/ ; npm run dev

# Start the backend
cd backend/ ; fastapi dev main.py
```

Start using application using Docker

```bash
docker-compose up --detach

# Restart the backend-fastapi container to apply server changes
docker-compose restart backend-fastapi
```

> **⚠️ Note:** For the backend API to work, you need to have Apache Jena Fuseki running on `http://localhost:3030` with a dataset named `Esolangs`.

<!-- Contributing -->
## :wave: Contributing

<a href="https://github.com/Vladimir-SS/ELAn_Esoteric-Language-Explorer/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Vladimir-SS/ELAn_Esoteric-Language-Explorer" />
</a>

<!-- License -->
## :warning: License

Distributed under the MIT License. See `LICENSE` for more information.
