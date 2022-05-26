#!/bin/bash

nodes_file='/etc/systemd/system/nodes'

#cat ./docker-compose.yml | grep hostname | grep node | awk '{print $2}' > $nodes_file

#echo_and_run() { echo "$@" ; $@ ; }
echo_and_run() { echo "$@" ; }


function create_resources_manually() {
    mem=$(grep -e "^MemTotal" /proc/meminfo | awk '{print $2}')
    mem=$((mem / 1024 / 1024 + 1))
    num_cpuset=$(grep -e "^processor\s\+:" /proc/cpuinfo | sort -u | wc -l)

    oarproperty -a cpu || true
    oarproperty -a core || true
    oarproperty -c -a host || true
    oarproperty -a mem || true

    cpu=1
    while read node; do
      for ((cpuset=0;cpuset<$num_cpuset; cpuset++)); do
        core=$((((cpu - 1) * num_cpuset) + cpuset + 1))
        echo_and_run oarnodesetting -a -h $node -p host=$node -p cpu=$cpu -p core=$core -p cpuset=$cpuset -p mem=$mem &
        wait

      done
      cpu=$((cpu + 1))
    done <$nodes_file
}


