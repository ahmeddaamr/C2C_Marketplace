pipeline {
    agent any 
    
    // environment {
    //     ENV = '.env'
    // }

    stages {
        stage('Checkout') {
            steps {
                echo 'Fetching code from repository...'
                //option 1
                // checkout scmGit(branches: [[name: 'main']], userRemoteConfigs: [[url: 'https://github.com/ahmeddaamr/C2C_Marketplace.git']])
                //option 2
                // checkout scm
                //option 3
                git branch: 'main',
                    url: 'https://github.com/ahmeddaamr/C2C_Marketplace.git',
                    credentialsId: 'github-pat'
            }
        }

        stage('Build') {
            steps {
                echo 'Compiling code and building artifact...'
                sh 'docker-compose up -d'
                echo 'Docker Compose ran successfully'
            }
        }

        stage('Integrate & Test') {
            steps {
                echo 'Running unit and integration tests...'
                sh 'docker exec c2c_marketplace_app python manage.py test'
            }
        }

    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
            // mail to: 'ahmedamrabdelsalam@gmail.com',
            //      subject: "Jenkins Build SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            //      body: 'The pipeline completed successfully.'

            // Teams notification example:
            // office365ConnectorSend webhookUrl: 'https://outlook.office.com/webhook/....',
            //     message: "Build succeeded for ${env.JOB_NAME} #${env.BUILD_NUMBER}" 
        }
        failure {
            echo 'Pipeline failed. Check the logs for errors.'
            // mail to: 'ahmedamrabdelsalam@gmail.com',
            //      subject: "Jenkins Build FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            //      body: 'The pipeline failed. Please check the Jenkins console output.'

            // Teams notification example:
            // office365ConnectorSend webhookUrl: 'https://outlook.office.com/webhook/....',
            //     message: "Build failed for ${env.JOB_NAME} #${env.BUILD_NUMBER}" 
        }
    }
}
