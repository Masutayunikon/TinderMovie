### Tinder Movies

Tinder Movies is a personalized movie recommendation system that leverages Semantic Web technologies and user interaction to suggest movies based on individual preferences. This README provides instructions for installing the required libraries and configuring parameters such as page limit and year limit for movie data retrieval.

#### Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   ```

2. **Install Dependencies:**
   ```bash
   pip install rdflib requests
   ```

#### Configuration

In the Python script provided (`main.py`) inside the script folder, you can adjust the following parameters:

1. **Page Limit for Movie Retrieval:**
    - Modify the `max` variable inside the `get_movie_by_year` function to set the maximum number of pages to retrieve from the API per year. This parameter controls how many movies are fetched for each year.

2. **Year Limit for Movie Retrieval:**
    - The `get_movie_by_year` function retrieves movies for a range of years. Adjust the range as needed to specify the years from which movies should be fetched.

#### Usage

1. **Run the Script:**
   ```bash
   python main.py
   ```
   This script populates the ontology with movie data fetched from The Movie Database (TMDb) API and saves the ontology to a file named `movies.owl`.

2. **Interact with the Application:**
    - After the ontology is populated, users can interact with the Tinder-like game interface to like or dislike movies presented to them.

3. **View Recommendations:**
    - Based on user interactions within the game, the application generates movie recommendations tailored to the user's preferences.

#### Contributing

Contributions to improve the functionality or add new features to Tinder Movies are welcome. Please fork the repository, make your changes, and submit a pull request with a detailed description of the modifications.

#### License

This project is licensed under the [MIT License](LICENSE).


### Docker Setup for SPARQL Endpoint with Jena Fuseki

This README provides instructions for setting up a SPARQL endpoint using Jena Fuseki Docker image. Follow the steps below to launch the Docker container and configure the SPARQL dataset.

#### Prerequisites

Before proceeding, ensure that you have Docker installed on your system. You can download and install Docker from the [official Docker website](https://www.docker.com/get-started).

#### Launching the Docker Container

1. **Pull the Jena Fuseki Docker Image:**
   ```bash
   docker pull stain/jena-fuseki
   ```

2. **Run the Docker Container:**
   ```bash
   docker run -p 3030:3030 -e ADMIN_PASSWORD=<your_password> stain/jena-fuseki
   ```
   Replace `<your_password>` with your desired admin password for accessing the Fuseki dashboard.

3. **Accessing the Fuseki Dashboard:**
    - Once the container is running, you can access the Fuseki dashboard by visiting `http://localhost:3030` in your web browser.
    - Log in using the default username `admin` and the password you provided in step 2.

#### Uploading Ontologies and Configuring SPARQL Dataset

1. **Upload Ontologies:**
    - Inside the Fuseki dashboard, navigate to the "Manage Datasets" section.
    - Click on "Add new dataset" and name the dataset "movies".
    - Upload the `movies.owl` ontology file or any other RDF data you wish to query using SPARQL.

2. **Configuring the Dataset:**
    - After adding the dataset, you can configure its properties such as dataset type and base URI.
    - Ensure that the dataset named "movies" is selected for querying RDF data related to movies.

#### Accessing SPARQL Endpoint

1. **Accessing the SPARQL Query Interface:**
    - With the Jena Fuseki container running, navigate to `http://localhost:3030/movies/sparql` in your web browser.
    - Here, you can execute SPARQL queries to retrieve data from the uploaded ontology or dataset.

2. **Querying RDF Data:**
    - Use the SPARQL query interface to write and execute queries against the "movies" dataset.
    - Explore the RDF data and retrieve information about movies, genres, actors, and more.

#### Additional Information

- **Dataset Maintenance:**
    - You can manage and update the "movies" dataset, including adding or removing RDF data, through the Fuseki dashboard.

- **Customization:**
    - Customize Fuseki configuration and Docker container parameters as needed for your specific use case.

#### Contributing

Contributions to enhance this Docker setup or improve the documentation are welcome. Please fork the repository, make your changes, and submit a pull request with a detailed description of the modifications.

#### License

This Docker setup is provided under the [MIT License](LICENSE).


# Nuxt 3 Minimal Starter

Look at the [Nuxt 3 documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.

## Setup

Make sure to install the dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm run dev

# yarn
yarn dev

# bun
bun run dev
```

## Production

Build the application for production:

```bash
# npm
npm run build

# pnpm
pnpm run build

# yarn
yarn build

# bun
bun run build
```

Locally preview production build:

```bash
# npm
npm run preview

# pnpm
pnpm run preview

# yarn
yarn preview

# bun
bun run preview
```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.

### Recommendations System Setup

This README provides instructions for setting up and running the recommendations system. Ensure you have the ontologies, Jena Fuseki, and Nuxt dependencies installed before proceeding.

#### Prerequisites

1. **Ontologies:**
    - Make sure you have the ontology files (e.g., `movies.owl`) ready for the recommendations system. These ontologies contain the RDF data used for generating recommendations.

2. **Jena Fuseki:**
    - Jena Fuseki should be installed and running to provide the SPARQL endpoint for querying RDF data from the ontologies.

3. **Nuxt Dependencies:**
    - Install the necessary dependencies for the Nuxt.js project, including Node.js and npm.

#### Launching the Recommendations System

1. **Build the Nuxt Project:**
    - Navigate to the root directory of your Nuxt.js project.
    - Run the following command to build the project:
      ```bash
      npm run build
      ```

2. **Preview the Nuxt Project:**
    - After successfully building the project, start the development server to preview the recommendations system:
      ```bash
      npm run preview
      ```

3. **Accessing the Recommendations System:**
    - Once the development server is running, open your web browser and go to `http://localhost:3000` to access the recommendations system.

#### Using the Recommendations System

1. **Explore Recommendations:**
    - Upon accessing the system, you will be presented with a user interface to explore movie recommendations.
    - Use the provided features and interfaces to browse, search, and discover movies based on your preferences.

2. **Interacting with Recommendations:**
    - Utilize the search functionality to find specific movies or genres.
    - Browse through recommended movies based on your previous interactions or preferences.

3. **Customizing Recommendations:**
    - Depending on the implementation, you may have options to customize or refine recommendations based on various factors such as genre preferences, ratings, or user profiles.

#### Additional Information

- **Ontology Integration:**
    - Ensure that the RDF data from the ontologies is correctly integrated and accessible within the Nuxt.js project for generating recommendations.

- **SPARQL Queries:**
    - The recommendations system may utilize SPARQL queries to retrieve relevant RDF data from the Jena Fuseki SPARQL endpoint.

- **Enhancements and Customization:**
    - Consider enhancing the recommendations system with additional features such as user authentication, personalized recommendations, or advanced search capabilities.

#### Contributing

Contributions to improve the recommendations system or enhance its functionality are welcome. Please fork the repository, make your changes, and submit a pull request with a detailed description of the modifications.

#### License

This recommendations system is provided under the [MIT License](LICENSE). Feel free to modify and adapt it to suit your specific requirements.
