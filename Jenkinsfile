pipeline {
    agent any

    stages {
        stage('Check environment') {
            steps {
                sh 'python3 --version'
                sh 'git --version'
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'python3 -m venv .venv'
                sh '.venv/bin/python -m pip install --upgrade pip'
                sh '.venv/bin/python -m pip install -r requirements.txt'
            }
        }


        stage('Smoke tests') {
            steps {
                sh 'source .venv/bin/activate'
                sh 'pytest -m smoke'
            }
        }

        stage('Run tests') {
            steps {
                sh '.venv/bin/python -m pytest -v --junitxml=results.xml'
            }

            post {
                always {
                    junit testResults: 'results.xml'
                }
            }
        }
    }
}