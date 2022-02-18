#!/bin/bash
set -uex

# The source to watch
SRCDIR=$1
# The folder  containing the copy
TMPDIR=$2

wait_oar_provision () {

  # After 60 seconds the loop will exit
  timeout=60

  while [ ! -f /oar_provisioned ];
  do
    # When the timeout is equal to zero, show an error and leave the loop.
    if [ "$timeout" == 0 ]; then
      echo "ERROR: Timeout while waiting for the file /oar_provisioned."
      exit 1
    fi

    sleep 1

    # Decrease the timeout of one
    ((timeout--))
  done
}

while true; do
  # To avoid systemd service deadlock,
  # we wait for provisioning to finish checking for the file generated by provisionning.sh
  wait_oar_provision

  inotifywait -e modify,create,delete,move -r ${SRCDIR} && \
    rsync -r ${SRCDIR}/* ${TMPDIR} && \
    cd ${TMPDIR} && /root/.poetry/bin/poetry build && \
    pip install dist/*.whl --force-reinstall

done