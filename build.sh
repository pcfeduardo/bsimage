#!/bin/bash
# Changes according to architecture 
PLATFORM="linux/amd64"

# Don't change this
TRIVY="$(which trivy)"
DOCKER="$(which docker)"
ECHO="$(which echo)"
IMAGETAG=$2
PATH=$3
DOCKERFILE=$4
EVIDENCE=${RANDOM}${RANDOM}.log

build(){
    echo "** Building..."
    ${DOCKER} image build -f ${PATH}/${DOCKERFILE} -t ${IMAGETAG} ${PATH} --platform=${PLATFORM} -q
}

banner(){
    ${ECHO} "** BSImage (build&scan image)"
    ${ECHO} "** build image and scan with trivy opensource"
}
scan(){
    echo "** Scanning..."
    $TRIVY image --exit-code 1 ${IMAGETAG} >> ${EVIDENCE}
    if [ $? == 0 ]
    then
        ${ECHO} "Approved! :)"
    else
        ${ECHO} "Not approved! :("
    fi
    ${ECHO} "You can check this evidence log file: ${EVIDENCE}"
}

case "$1" in
    "start")
        banner
        if [ -z $2 ] || [ -z $3 ] || [ -z $4 ] 
        then
            ${ECHO} "** Missing parameters"
            exit 1
        fi
        ${ECHO} "** Starting..."
        build
        scan
;;

*)
    banner
    ${ECHO} ""
    ${ECHO} "Usage: $0 { start <image:tag> <dir_path> <dockerfile> }"
    ${ECHO} ""
;;
esac