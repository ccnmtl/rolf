// Sandbox approvals that you will need (at least):
// staticMethod org.codehaus.groovy.runtime.DefaultGroovyMethods plus java.lang.Object[]
// staticMethod org.codehaus.groovy.runtime.DefaultGroovyMethods getAt java.lang.Iterable int
// java.lang.Object[]
// staticMethod org.codehaus.groovy.runtime.DefaultGroovyMethods plus java.util.List java.lang.Object

TAG = 'build-' + env.BUILD_NUMBER
env.TAG = TAG

// check for required parameters. assign them to the env for
// convenience and make sure that an exception is raised if any
// are missing as a side-effect

env.APP = APP
env.REPO = REPO
env.ADMIN_EMAIL = ADMIN_EMAIL

def hosts = HOSTS.split(" ")

// optional (not all apps use celery/beat)
def celery_hosts = [:]
def beat_hosts = [:]
try {
    celery_hosts = CELERY_HOSTS.split(" ")
    beat_hosts = BEAT_HOSTS.split(" ")
} catch (hostsErr) {
    // don't care
    celery_hosts = []
    beat_hosts = []
}
def all_hosts = hosts + celery_hosts + beat_hosts as Set

def smoketestURL = null
try {
    smoketestURL = SMOKETEST_URL
} catch (smoketestURLError) {
    smoketestURL = "https://${APP}.ccnmtl.columbia.edu/smoketest/"
}

def mediacheckURL = null
try {
    mediacheckURL = MEDIACHECK_URL
} catch (mediacheckURLError) {
    mediacheckURL = "https://${APP}.ccnmtl.columbia.edu/"
}

def mediacheckTimeout = 10
try {
    mediacheckTimeout = MEDIACHECK_TIMEOUT
} catch (mediacheckTimeoutError) {
    mediacheckTimeout = 10
}

def mediacheckVerify = ''
try {
    if (MEDIACHECK_SKIP_VERIFY) {
        mediacheckVerify = '--verify-ssl=false'
    }
} catch (mediacheckVerifyError) {
}

def opbeat = true
try {
    env.OPBEAT_ORG = OPBEAT_ORG
    env.OPBEAT_APP = OPBEAT_APP
    // OPBEAT_TOKEN comes out of credential store
} catch (opbeatErr) {
    println "opbeat not configured"
    opbeat = false
}


def err = null
currentBuild.result = "SUCCESS"

try {
    node {
        stage 'Checkout'
        checkout scm

        stage "Build"
        sh "docker pull ${REPO}/${APP}:latest"
        sh "make build"
        sh "rm -rf reports/"
        sh """container=\$(docker create ${REPO}/${APP}:${TAG})
docker cp \$container:/app/reports reports/
docker rm \$container
touch reports/*
"""

        stage "Unit Tests"
        junit "reports/junit.xml"

        // TODO: coverage/pep8

        stage "Docker Push"
        retry_backoff(5) { sh "docker push ${REPO}/${APP}:${TAG}" }
    }

    node {
        def branches = [:]
        stage "Docker Pull"

        for (int i = 0; i < all_hosts.size(); i++) {
            def host = all_hosts[i]
            branches["pull-${i}"] = {
                node {
                    sh "ssh ${host} docker pull \${REPOSITORY}\$REPO/${APP}:\$TAG"
                }
            }
        }
        parallel branches

        stage "Migrate"
        def host = all_hosts[0]
        sh "ssh ${host} /usr/local/bin/docker-runner ${APP} migrate"

        stage "Collectstatic"
        sh "ssh ${host} /usr/local/bin/docker-runner ${APP} collectstatic"

        stage "Compress"
        sh "ssh ${host} /usr/local/bin/docker-runner ${APP} compress"
    }

    node {
        stage "restart gunicorn"
        def branches = [:]
        for (int i = 0; i < hosts.size(); i++) {
            branches["web-restart-${i}"] = create_restart_web_exec(i, hosts[i])
        }
        parallel branches
    }

    if (celery_hosts.size() > 0) {
        node {
            stage "restart celery worker"
            def branches = [:]
            for (int i = 0; i < celery_hosts.size(); i++) {
                branches["celery-restart-${i}"] = create_restart_celery_exec(i, celery_hosts[i])
            }
            parallel branches
        }
    }

    if (beat_hosts.size() > 0) {
        node {
            stage "restart celery beat"
            def branches = [:]
            for (int i = 0; i < beat_hosts.size(); i++) {
                branches["beat-restart-${i}"] = create_restart_beat_exec(i, beat_hosts[i])
            }
            parallel branches
        }
    }

    node {
        if (smoketestURL != null) {
            stage "smoketest"
            retry_backoff(5) { sh """#!/bin/bash
curl ${smoketestURL} --silent | grep PASS
"""
            }
        }

        if (mediacheckURL != null) {
            stage "mediacheck"
            retry_backoff(5) { sh "mediacheck --url='${mediacheckURL}' --log-level=info --timeout=${mediacheckTimeout * 1000} ${mediacheckVerify}" }
        }
    }

    if (opbeat) {
        node {
            stage "Opbeat"
            withCredentials([[$class: 'StringBinding', credentialsId : APP + '-opbeat', variable: 'OPBEAT_TOKEN', ]]) {
                sh '''curl https://intake.opbeat.com/api/v1/organizations/${OPBEAT_ORG}/apps/${OPBEAT_APP}/releases/ \
       -H "Authorization: Bearer ${OPBEAT_TOKEN}" \
       -d rev=`git log -n 1 --pretty=format:%H` \
       -d branch=`git rev-parse --abbrev-ref HEAD` \
       -d status=completed'''
            }
        }
    }
} catch (caughtError) {
    err = caughtError
    currentBuild.result = "FAILURE"
} finally {
    (currentBuild.result != "ABORTED") && node {
        notifyBuild(currentBuild.result)
    }

    /* Must re-throw exception to propagate error */
    if (err) {
        throw err
    }
}

// -------------------- helper functions ----------------------

def notifyBuild(String buildStatus = 'STARTED') {
		// build status of null means successful
		buildStatus =  buildStatus ?: 'SUCCESS'

		// Default values
		def colorCode = '#FF0000'
		def subject = "${buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
		def summary = "${subject} (${env.BUILD_URL})"
		def details = """<p>STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
    <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>"""

		// Override default values based on build status
		if (buildStatus == 'STARTED') {
				color = 'YELLOW'
				colorCode = '#FFFF00'
		} else if (buildStatus == 'SUCCESS') {
				color = 'GREEN'
				colorCode = '#36a64f'
		} else {
				color = 'RED'
				colorCode = '#FF0000'
		}

		// Send notifications
		//  slackSend (color: colorCode, message: summary)

		step([$class: 'Mailer',
					notifyEveryUnstableBuild: true,
					recipients: ADMIN_EMAIL,
					sendToIndividuals: true])
}

def create_restart_web_exec(int i, String host) {
    cmd = {
        node {
            sh """
ssh ${host} sudo stop ${APP} || true
ssh ${host} sudo start ${APP}
"""
        }
    }
    return cmd
}

def create_restart_celery_exec(int i, String host) {
    cmd = {
        node {
            sh """
ssh ${host} sudo stop ${APP}-worker || true
ssh ${host} sudo start ${APP}-worker
"""
				}
    }
    return cmd
}

def create_restart_beat_exec(int i, String host) {
    cmd = {
        node {
            sh """
ssh ${host} sudo stop ${APP}-beat || true
ssh ${host} sudo start ${APP}-beat
"""
        }
    }
    return cmd
}

// retry with exponential backoff
def retry_backoff(int max_attempts, Closure c) {
    int n = 0
    while (n < max_attempts) {
        try {
            c()
            return
        } catch (err) {
            if ((n + 1) >= max_attempts) {
                // we're done. re-raise the exception
                throw err
            }
            sleep(2**n)
            n++
								}
    }
    return
}
