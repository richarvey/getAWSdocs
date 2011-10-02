#!/bin/bash
# Richard Harvey richard at squarecows dot com
# version 1.1 2001/07/06

function download_latest()
{
    STG=$1
    DOCS=$(curl -s http://aws.amazon.com/documentation/${STG}/ | grep href | grep pdf | awk -F '"' '{print $2}' | uniq)
    for get_doc in ${DOCS}
    do
        doc_name=$(echo ${get_doc} | awk -F 'latest/' '{print $1}')
        if [ ! -a ${BASEDIR}/${STG}/${doc_name} ]; then
            wget -P ${BASEDIR}/${STG}/ ${get_doc}
        else
            echo "${doc_name} is the latest version"
        fi
    done
}

### MAIN ##
REMOVE=0

while getopts ":r" opt
do
  case $opt in
    r)
      echo "Removing Old Files"
      REMOVE=1
      ;;
  esac
done

# Clear old variables
unset SERVICES
unset DOCS
unset STG
BASEDIR="documents"

# Make a list of available services from AWS
SERVICES=$(curl -s http://aws.amazon.com/documentation/ | grep "a href=\"./" | awk -F '/' '{print $2}')

if [ ${REMOVE} -eq 1 ]; then
    rm -Rf ${BASEDIR}
fi

if [ ! -d ${BASEDIR} ]; then 
    mkdir ${BASEDIR}
    #hack to prevent race condition
    sleep 2
fi
for service in ${SERVICES}
do
    if [ ! -d ${BASEDIR}/${service} ]; then
        echo "### Creating New Service Directory: ${service}"
        mkdir ${BASEDIR}/${service}
    fi
    
# Now get the documents for the servcie
 download_latest ${service}
done
