# Readme for Makefile

This Makefile provides a set of commands for managing a Dockerized application and deploying it to Kubernetes. Additionally, it includes instructions on how to set up a development environment using the Docker Compose file (`src/docker-compose.yaml`), configure AWS on macOS and Linux for deploying to Amazon EKS, and deploy Kubernetes resources using Terraform. Below is a description of each target and the steps to utilize the Docker Compose file for development, as well as AWS and Terraform configuration instructions:

### Targets:

1. `stop`:
   - Description: Stops the Docker containers specified in the `docker-compose.yaml` file.
   - Usage: `make stop`

2. `start`:
   - Description: Builds and starts the Docker containers defined in the `docker-compose.yaml` file.
   - Usage: `make start`

3. `test`:
   - Description: Builds and runs tests using Docker Compose.
   - Usage: `make test`

4. `build`:
   - Description: Builds a Docker image for the application and pushes it to a Docker registry.
   - Usage: `make build version=<version>`, where `<version>` is the version tag for the Docker image.

5. `configk8s`:
   - Description: Configures kubectl to work with an Amazon EKS cluster.
   - Usage: `make configk8s`

6. `deployk8s`:
   - Description: Deploys the Kubernetes resources defined in the `terraform` directory to the configured EKS cluster.
   - Usage: `make deployk8s`

7. `distroyk8s`:
   - Description: Destroys the Kubernetes resources provisioned on the EKS cluster using Terraform.
   - Usage: `make distroyk8s`

8. `applyingress`:
   - Description: Installs an Ingress controller for the Kubernetes cluster using Helm and applies the Ingress configuration specified in `k8s/ingress-nginx/values-prod.yaml`.
   - Usage: `make applyingress`

9. `applyk8s`:
   - Description: Applies the Kubernetes namespace and application resources defined in the `k8s` directory to the Kubernetes cluster.
   - Usage: `make applyk8s`

### Setting up Development Environment using Docker Compose:

To use the `docker-compose.yaml` file for developing the application locally, follow these steps:

1. **Install Docker and Docker Compose**:
   Ensure that you have Docker and Docker Compose installed on your development machine. If you don't have them installed, you can download and install them from the official Docker website (https://www.docker.com/).

2. **Clone the Repository**:
   Clone the repository containing the application source code and the `docker-compose.yaml` file to your local development environment.

3. **Build and Start the Application**:
   In the root directory of the cloned repository, use the following command to build and start the application using Docker Compose:
   ```
   make start
   ```

   This command will pull the required Docker images, build the application's Docker image, and start the application containers defined in the `docker-compose.yaml` file. The application should now be running locally and accessible on the specified ports.

4. **Development Workflow**:
   - Make changes to your application's source code using your favorite code editor or IDE.
   - Save the changes.
   - The changes will be automatically reflected inside the Docker containers, allowing you to test and debug the application in the development environment.

5. **Stop the Application**:
   To stop the application and its associated containers, use the following command:
   ```
   make stop
   ```

   This command will gracefully stop the running containers without removing them, allowing you to resume development later.

### Prerequisites:
- Docker is installed and running on the local machine.
- Docker Compose is installed on the local machine.
- The application's source code and the `docker-compose.yaml` file are available in the local development environment.

### Configuring AWS on macOS and Linux:

To configure AWS for deploying to Amazon EKS, follow these steps:

1. **Install the AWS CLI**:
   - For macOS, you can install the AWS CLI using Homebrew with the following command:
     ```
     brew install awscli
     ```

   - For Linux, you can install the AWS CLI using the package manager for your distribution (e.g., apt, yum, dnf). For example, on Ubuntu, you can use the following command:
     ```
     sudo apt-get update
     sudo apt-get install awscli
     ```

2. **Configure AWS Credentials**:
   After installing the AWS CLI, you need to configure your AWS credentials to access your AWS resources. Run the following command and follow the prompts:
   ```
   aws configure
   ```

   You will be asked to provide your AWS Access Key ID, Secret Access Key, default region name, and default output format. These credentials will be used by various AWS CLI commands to authenticate your requests.

3. **Install kubectl**:
   kubectl is a command-line tool used to interact with Kubernetes clusters. You can install it using various package managers or download the binary directly from the Kubernetes website. For example, on macOS, you can install kubectl using Homebrew with the following command:
   ```
   brew install kubectl
   ```

4. **Configure kubectl for Amazon EKS**:
   The Makefile includes a target `configk8s`, which automates the process of configuring kubectl to work with your Amazon EKS cluster. To configure kubectl, use the following command:
   ```
   make configk8s
   ```

   This target will use the AWS CLI to update kubectl's configuration to connect to the specified Amazon EKS cluster. The configuration includes the authentication credentials, cluster endpoint, and context name.

### Deploying Kubernetes Resources using Terraform:

To deploy the Kubernetes resources to your Amazon EKS cluster using Terraform, follow these steps:

1. **Install Terraform**:
   Make sure Terraform is installed on your development machine. You can download the appropriate Terraform binary for your OS from the Terraform website (https://www.terraform.io/downloads.html) and add it to your system's PATH.

2. **Initialize Terraform**:
   In the `terraform` directory, run the following command to initialize Terraform and download the required providers and modules:
   ```
   terraform init
   ```

3. **Plan and Apply**:
   Once Terraform is initialized, you can use the following commands to see the execution plan and apply the changes to your EKS cluster:
   ```
   terraform plan
   terraform apply
   ```

   The `terraform plan` command will show you the changes that Terraform will apply. Review the plan to ensure it aligns with your expectations. Then, use `terraform apply` to apply the changes and create the Kubernetes resources on your EKS cluster.

### Cleaning up Kubernetes Resources using Terraform:

To clean up and remove the Kubernetes resources provisioned on your EKS cluster using Terraform, follow these steps:

1. **Destroy Resources**:
   In the `terraform` directory, run the following command to destroy the Kubernetes resources and remove them from your EKS cluster:
   ```
   terraform destroy
   ```

   Terraform will prompt you to confirm the destruction. Enter `yes` when

## GitHub Actions Workflow (Docker Image CI)

The repository includes a GitHub Actions workflow that automates the building and pushing of Docker images to Docker Hub when changes are made to the `main` branch or when pull requests are submitted targeting the `main` branch.

### Workflow Description:

- The workflow is defined in the `.github/workflows/docker-image-ci.yml` file.
- It uses the `ubuntu-latest` runner to execute the CI tasks on an Ubuntu environment.

### Workflow Triggers:

The workflow is triggered by the following events:

- `push` events to the `main` branch.
- `pull_request` events targeting the `main` branch.

### Workflow Jobs:

1. **Build and Push Docker Image:**

   This job builds the Docker image for the application and pushes it to Docker Hub. The steps in this job are as follows:

   - `Checkout code`: Checks out the code from the repository.
   - `Run Unit Tests`: Runs unit tests for the application using the `make test` command from the `Makefile`.
   - `Log in to Docker Hub`: Logs in to Docker Hub using the `docker/login-action` with the provided Docker Hub credentials stored in GitHub secrets. This step authenticates the workflow to push the Docker image to Docker Hub.
   - `Build and push Docker image`: Uses the `docker/build-push-action` to build and push the Docker image to Docker Hub. The image is tagged with the format `DOCKER_USERNAME/hemnet-task-app:github.run_id`. The `DOCKER_USERNAME` is a secret that holds the Docker Hub username, and `github.run_id` is the unique identifier for the workflow run.

2. **Build and Push Docker Image (latest tag):**

   This job builds and pushes the Docker image with the `latest` tag to Docker Hub. The steps are similar to the previous job, but the image is tagged with the format `DOCKER_USERNAME/hemnet-task-app:latest`.

### GitHub Secrets:

The workflow uses the following GitHub secrets:

- `DOCKER_USERNAME`: The Docker Hub username used to log in and push the Docker image.
- `DOCKER_HUB_TOKEN`: The Docker Hub access token used to authenticate the workflow.

### Automation Test and Docker Image Push:

1. The workflow begins by running the unit tests for the application using the `make test` command from the `Makefile`.

2. Once the unit tests are successful, the workflow proceeds to build and push the Docker image with a unique tag based on the `github.run_id`. This allows for versioning of the Docker image based on the workflow run.

3. Additionally, the workflow also builds and pushes another Docker image tagged as `latest`. This is typically used as a versionless reference to the most recent image, making it convenient for deployment scenarios.

