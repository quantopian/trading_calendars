#!/bin/bash
#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------
#
# Docs: https://github.com/microsoft/vscode-dev-containers/blob/master/script-library/docs/node.md
#
# Syntax: ./node-debian.sh [directory to install nvm] [node version to install (use "none" to skip)] [non-root user] [Update rc files flag]

export NVM_DIR=${1:-"/usr/local/share/nvm"}
export NODE_VERSION=${2:-"lts/*"}
USERNAME=${3:-"automatic"}
UPDATE_RC=${4:-"true"}

set -e

if [ "$(id -u)" -ne 0 ]; then
    echo -e 'Script must be run as root. Use sudo, su, or add "USER root" to your Dockerfile before running this script.'
    exit 1
fi

# Determine the appropriate non-root user
if [ "${USERNAME}" = "auto" ] || [ "${USERNAME}" = "automatic" ]; then
    USERNAME=""
    POSSIBLE_USERS=("vscode" "node" "codespace" "$(awk -v val=1000 -F ":" '$3==val{print $1}' /etc/passwd)")
    for CURRENT_USER in ${POSSIBLE_USERS[@]}; do
        if id -u ${CURRENT_USER} > /dev/null 2>&1; then
            USERNAME=${CURRENT_USER}
            break
        fi
    done
    if [ "${USERNAME}" = "" ]; then
        USERNAME=root
    fi
elif [ "${USERNAME}" = "none" ] || ! id -u ${USERNAME} > /dev/null 2>&1; then
    USERNAME=root
fi

if [ "${NODE_VERSION}" = "none" ]; then
    export NODE_VERSION=
fi

# Ensure apt is in non-interactive to avoid prompts
export DEBIAN_FRONTEND=noninteractive

# Install curl, apt-transport-https, tar, or gpg if missing
if ! dpkg -s apt-transport-https curl ca-certificates tar > /dev/null 2>&1 || ! type gpg > /dev/null 2>&1; then
    if [ ! -d "/var/lib/apt/lists" ] || [ "$(ls /var/lib/apt/lists/ | wc -l)" = "0" ]; then
        apt-get update
    fi
    apt-get -y install --no-install-recommends apt-transport-https curl ca-certificates tar gnupg2
fi

# Install yarn
if type yarn > /dev/null 2>&1; then
    echo "Yarn already installed."
else
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | (OUT=$(apt-key add - 2>&1) || echo $OUT)
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
    apt-get update
    apt-get -y install --no-install-recommends yarn
fi

# Install the specified node version if NVM directory already exists, then exit
if [ -d "${NVM_DIR}" ]; then
    echo "NVM already installed."
    if [ "${NODE_VERSION}" != "" ]; then
       su ${USERNAME} -c "source $NVM_DIR/nvm.sh && nvm install ${NODE_VERSION} && nvm clear-cache"
    fi
    exit 0
fi


# Run NVM installer as non-root if needed
mkdir -p ${NVM_DIR}
chown ${USERNAME} ${NVM_DIR}
su ${USERNAME} -c "$(cat << EOF
    set -e

    # Do not update profile - we'll do this manually
    export PROFILE=/dev/null

    curl -so- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash 
    source ${NVM_DIR}/nvm.sh
    if [ "${NODE_VERSION}" != "" ]; then
        nvm alias default ${NODE_VERSION}
    fi
    nvm clear-cache 
EOF
)" 2>&1

if [ "${UPDATE_RC}" = "true" ]; then
    echo "Updating /etc/bash.bashrc and /etc/zsh/zshrc with NVM scripts..."
(cat <<EOF
export NVM_DIR="${NVM_DIR}"
sudoIf()
{
    if [ "\$(id -u)" -ne 0 ]; then
        sudo "\$@"
    else
        "\$@"
    fi
}
if [ "\$(stat -c '%U' \$NVM_DIR)" != "${USERNAME}" ]; then
    if [ "\$(id -u)" -eq 0 ] || type sudo > /dev/null 2>&1; then
        echo "Fixing permissions of \"\$NVM_DIR\"..."
        sudoIf chown -R ${USERNAME}:root \$NVM_DIR
    else
        echo "Warning: NVM directory is not owned by ${USERNAME} and sudo is not installed. Unable to correct permissions."
    fi
fi
[ -s "\$NVM_DIR/nvm.sh" ] && . "\$NVM_DIR/nvm.sh"
[ -s "\$NVM_DIR/bash_completion" ] && . "\$NVM_DIR/bash_completion"
EOF
) | tee -a /etc/bash.bashrc >> /etc/zsh/zshrc 
fi 

echo "Done!"