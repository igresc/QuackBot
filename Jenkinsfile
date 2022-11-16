pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                metadata:
                    namespace: jenkins
                spec:
                    containers:
                        - name: golang
                          image: golang:1.18.2
                          command:
                              - sleep
                          args:
                              - 99d
                        - name: docker
                          image: "docker:20.10.21-dind-alpine3.16"
                          imagePullPolicy: Always
                          command: ["dockerd"]
                          env:
                            - name: "DOCKER_HOST"
                              value: "tcp://docker:2375"
                          securityContext:
                              privileged: true
            '''
            defaultContainer 'golang'
        }
    }
    environment {
        IMAGE_REPO = "igresc/quackbot"
    }
    stages {
/*         stage('Build') {
            steps {
                sh '''
                CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o bin/hello-server .
                go test -cover
                '''
            }
        } */
        stage("Build Docker Image") {
            environment {
                token = credentials("docker-hub")
            }
            steps {
                container('docker') {
                    sh 'echo $DOCKER_HOST'
                    sh 'docker context ls'
                    sh 'docker build . -t "${IMAGE_REPO}:${GIT_COMMIT}"'
                    sh 'docker login -u igresc -p $token_PSW'
                    sh 'docker push "${IMAGE_REPO}:${GIT_COMMIT}"'
                }
            }
        }
        stage("Deploy") {
            environment {
                GIT_CREDS = credentials('gitea-igresc')
                GIT_REPO_EMAIL = 'sergicastro2001@gmail.com'
                GIT_REPO_BRANCH = "main"
                GIT_REPO_DIR = "Quackbot"
            }
            steps {
                container('golang') {
                        git branch: 'main', credentialsId: 'gitea-igresc', url: 'https://git.local.isabelsoler.es/igresc/GitOps-deployments.git'
                        sh "pwd"
                        sh "ls -la"
                        //sh('git clone https://$GIT_CREDS_USR:$GIT_CREDS_PSW@git.local.isabelsoler.es/$GIT_CREDS_USR/GitOps-deployments.git')
                        sh "git config --global user.email ${env.GIT_REPO_EMAIL}"
                        // install yq
                        sh "wget https://github.com/mikefarah/yq/releases/download/v4.9.6/yq_linux_amd64.tar.gz"
                        sh "tar xvf yq_linux_amd64.tar.gz"
                        sh "mv yq_linux_amd64 /usr/bin/yq"
                        dir("Quackbot"){
                            sh "git checkout ${env.GIT_REPO_BRANCH}"
                            //install done
                            sh '''#!/bin/bash
                            echo $GIT_REPO_EMAIL
                            echo GIT_COMMIT $GIT_COMMIT
                            pwd
                            ls -lth 
                            yq eval '.spec.template.spec.containers[0].image = env(IMAGE_REPO) +":"+ env(GIT_COMMIT)' -i deployment.yaml
                            yq eval '.spec.template.spec.containers[0].env.[0].value = env(GIT_COMMIT)' -i deployment.yaml
                            cat deployment.yaml
                            pwd
                            git add deployment.yaml
                            git commit -m 'Triggered Build'
                            git push https://$GIT_CREDS_USR:$GIT_CREDS_PSW@git.local.isabelsoler.es/$GIT_CREDS_USR/GitOps-deployments.git
                            '''
                        }
                }
            }
        }
    }
}