#!/usr/bin/env groovy

properties([
  buildDiscarder(logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '7', numToKeepStr: '')),
  pipelineTriggers([cron('H 1 * * *')])
])

node {
  catchError {
    env.ECR_REGISTRY = "825303761615.dkr.ecr.ap-southeast-1.amazonaws.com"
    env.APPLICATION_NAME = "api-test"

    stage('Clone repository') {
      def scmVars = checkout([
        $class: 'GitSCM',
        branches: scm.branches,
        extensions: scm.extensions + [
          [$class: 'CloneOption', honorRefspec: true, noTags: false],
          [$class: 'CleanCheckout']
        ],
        userRemoteConfigs: scm.userRemoteConfigs
      ])
    }

    env.APPLICATION_VERSION = sh(returnStdout: true, script: 'git describe --always --abbrev=8 HEAD').trim()
    stage("Build image: ${APPLICATION_NAME}") {
      withCredentials([string(credentialsId: 'vault_role_id', variable: 'ROLE_ID'), string(credentialsId: 'vault_jenkins_token', variable: 'VAULT_TOKEN')]) {
        sshagent (['user-app-keeper-ssh-key']) {
            sh '''
            set +x
            ./scripts/docker-build.sh ${APPLICATION_NAME} ${APPLICATION_VERSION}
            '''
        }
      }
      echo "Using image tag: ${APPLICATION_VERSION}"
      // push to ECR
    //   withCredentials([string(credentialsId: 'app_keeper_aws_access_key_id', variable: 'AWS_ACCESS_KEY_ID'),
    //                   string(credentialsId: 'app_keeper_aws_secret_access_key', variable: 'AWS_SECRET_ACCESS_KEY')]) {
    //     sh '''
    //     docker tag "${APPLICATION_NAME}:${APPLICATION_VERSION}" "${ECR_REGISTRY}/${APPLICATION_NAME}:${APPLICATION_VERSION}"
    //     docker tag "${APPLICATION_NAME}:${APPLICATION_VERSION}" "${ECR_REGISTRY}/${APPLICATION_NAME}:latest"
    //     docker push "${ECR_REGISTRY}/${APPLICATION_NAME}:${APPLICATION_VERSION}"
    //     docker push "${ECR_REGISTRY}/${APPLICATION_NAME}:latest"
    //     '''
    //   }
    }
    stage("Run test"){
      image = docker.image("${APPLICATION_NAME}:${APPLICATION_VERSION}")
      image.inside("") {
        sh '''
            set +x
            set -a
            ./scripts/run-test.sh
        '''
      }

      // publish html
      // snippet generator doesn't include "target:"
      // https://issues.jenkins-ci.org/browse/JENKINS-29711.
      // publishHTML (target: [
      //   allowMissing: true,
      //   alwaysLinkToLastBuild: true,
      //   keepAll: true,
      //   reportDir: 'reports',
      //   reportFiles: '*.html',
      //   reportName: "HttpRunner Report"
      // ])
      archiveArtifacts 'reports/*.html'
      findText alsoCheckConsoleOutput: true, regexp: '^FAILED', succeedIfFound: false, unstableIfFound: true
    }
  }
  notifyBuild(currentBuild.result)
}

def notifyBuild(String buildStatus = 'STARTED') {
  // build status of null means successful
  buildStatus = buildStatus ?: 'SUCCESS'
  gitCommit = sh(returnStdout: true, script: 'git describe --always --abbrev=8 HEAD').trim()
  commitChangeset = sh(returnStdout: true, script: 'git log --oneline -1').trim()
  // Default values
  def subject = "${buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
  def summary = """- Job     : ${env.JOB_NAME}
                  |- Version : ${gitCommit}
                  |- Commit  : ${commitChangeset}""".stripMargin()

  def recipient = "team.tech@castlery.com"
  mail (subject: subject,
          body: """Job: ${env.JOB_NAME}
                  |Build: ${env.BUILD_NUMBER}
                  |Status: ${buildStatus}
                  |Build URL: ${env.BUILD_URL}
                """.stripMargin(),
            to: recipient,
      replyTo: recipient,
          from: 'Jenkins <jenkins.noreply@castlery.com>')
}
