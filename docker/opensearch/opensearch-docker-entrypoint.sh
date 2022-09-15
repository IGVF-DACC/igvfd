#!/bin/bash

# Copied from https://github.com/opensearch-project/opensearch-build/blob/4597d77956a8d70905e03d135618de0ae912b316/docker/release/config/opensearch/opensearch-docker-entrypoint.sh
# to remove performance analyzer

# Export OpenSearch Home
export OPENSEARCH_HOME=/usr/share/opensearch
export OPENSEARCH_PATH_CONF=$OPENSEARCH_HOME/config

export OPENSEARCH_JAVA_OPTS="-Dopensearch.cgroups.hierarchy.override=/ $OPENSEARCH_JAVA_OPTS"

declare OPENSEARCH_PID

##Security Plugin
function setupSecurityPlugin {
    SECURITY_PLUGIN="opensearch-security"

    if [ -d "$OPENSEARCH_HOME/plugins/$SECURITY_PLUGIN" ]; then
        if [ "$DISABLE_INSTALL_DEMO_CONFIG" = "true" ]; then
            echo "Disabling execution of install_demo_configuration.sh for OpenSearch Security Plugin"
        else
            echo "Enabling execution of install_demo_configuration.sh for OpenSearch Security Plugin"
            bash $OPENSEARCH_HOME/plugins/$SECURITY_PLUGIN/tools/install_demo_configuration.sh -y -i -s
        fi

        if [ "$DISABLE_SECURITY_PLUGIN" = "true" ]; then
            echo "Disabling OpenSearch Security Plugin"
            opensearch_opt="-Eplugins.security.disabled=true"
            opensearch_opts+=("${opensearch_opt}")
        else
            echo "Enabling OpenSearch Security Plugin"
        fi
    fi
}

# Trap function that is used to terminate opensearch
# when a relevant signal is caught.
function terminateProcesses {
    if kill -0 $OPENSEARCH_PID >& /dev/null; then
        echo "Killing opensearch process $OPENSEARCH_PID"
        kill -TERM $OPENSEARCH_PID
        wait $OPENSEARCH_PID
    fi
}

# Start up the opensearch
# When either of them halts, this script exits, or we receive a SIGTERM or SIGINT signal then we want to kill both these processes.
function runOpensearch {
    # Files created by OpenSearch should always be group writable too
    umask 0002

    if [[ "$(id -u)" == "0" ]]; then
        echo "OpenSearch cannot run as root. Please start your container as another user."
        exit 1
    fi

    # Parse Docker env vars to customize OpenSearch
    #
    # e.g. Setting the env var cluster.name=testcluster
    # will cause OpenSearch to be invoked with -Ecluster.name=testcluster
    opensearch_opts=()
    while IFS='=' read -r envvar_key envvar_value
    do
        # OpenSearch settings need to have at least two dot separated lowercase
        # words, e.g. `cluster.name`, except for `processors` which we handle
        # specially
        if [[ "$envvar_key" =~ ^[a-z0-9_]+\.[a-z0-9_]+ || "$envvar_key" == "processors" ]]; then
            if [[ ! -z $envvar_value ]]; then
            opensearch_opt="-E${envvar_key}=${envvar_value}"
            opensearch_opts+=("${opensearch_opt}")
            fi
        fi
    done < <(env)

    setupSecurityPlugin

    # Enable job control so we receive SIGCHLD when a child process terminates
    set -m

    # Make sure we terminate the child processes in the event of us received TERM (e.g. "docker container stop"), INT (e.g. ctrl-C), EXIT (this script terminates for an unexpected reason), or CHLD (one of the processes terminated unexpectedly)
    trap terminateProcesses TERM INT EXIT CHLD

    # Start opensearch
    "$@" "${opensearch_opts[@]}" &
    OPENSEARCH_PID=$!

    # Wait for the child processes to terminate
    wait $OPENSEARCH_PID
    local opensearch_exit_code=$?
    echo "OpenSearch exited with code ${opensearch_exit_code}"

}

# Prepend "opensearch" command if no argument was provided or if the first
# argument looks like a flag (i.e. starts with a dash).
if [ $# -eq 0 ] || [ "${1:0:1}" = '-' ]; then
    set -- opensearch "$@"
fi

if [ "$1" = "opensearch" ]; then
    # If the first argument is opensearch, then run the setup script.
    runOpensearch "$@"
else
    # Otherwise, just exec the command.
    exec "$@"
fi
