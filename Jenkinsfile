node {
    def app
    def dockerHubUsername = 'gyanesh29'
    def dockerImageName = 'kidney-classification-app'
    def dockerTag = "${dockerHubUsername}/${dockerImageName}:latest"

    stage('Clone repository') {
        /* Cloning the repository into the workspace */
        checkout scm
    }

    stage('Build Docker Image') {
        /* Building the Docker image */
        app = docker.build(dockerTag, "-f Dockerfile .")
    }

    stage('Run Docker Container') {
        /* Running the Docker container */
        app.run("-it -p 8501:8501")
    }
}
