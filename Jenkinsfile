pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        COMPOSE_FILE = 'docker-compose.yaml'
        APP_CONTAINER = 'c2c_marketplace_app'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'

                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/ahmeddaamr/C2C_Marketplace.git',
                        credentialsId: 'github-pat'
                    ]]
                ])
            }
        }

        stage('Verify Environment') {
            steps {
                sh '''
                    pwd
                    ls -la
                    git branch
                    docker version
                '''
                    // docker compose version
            }
        }

        stage('Build & Deploy') {
            steps {
                echo 'Starting Docker Compose...'
                withCredentials([file(credentialsId: '.env', variable: 'ENV_FILE')]) {
                sh '''
                    cp "$ENV_FILE" .env
                    trap "rm -f .env" EXIT
            
                    docker compose -f docker-compose.yaml up -d --build
                '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Django tests...'

                sh '''
                    docker exec ${APP_CONTAINER} python manage.py test
                '''
            }
        }
    }

    post {

        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed.'
        }

        always {
            sh 'docker ps -a || true'
        }
    }
}