#!/bin/bash
# Changes according to architecture 
PLATFORM="linux/amd64"

# Don't change this
TRIVY="$(which trivy)"
DOCKER="$(which docker)"
ECHO="$(which echo)"
PLATFORM="linux/amd64"
BASENAME="$(which basename)"
TR="$(which tr)"
DIRLOG="$PWD/log"
DIR="$(which mkdir)"

if [ -z "$2" ]; then
    IMAGETAG=$(echo $($BASENAME $PWD) | ($TR A-Z a-z))  
    EVIDENCE=$IMAGETAG-${RANDOM}.log
    PATH=$PWD
    DOCKERFILE="dockerfile"
else
    PATH=$3
    DOCKERFILE=$4
    EVIDENCE=$2_${RANDOM}.log
    IMAGETAG=$2
fi


build(){
    echo $'\342\232\231' " Building..."
    echo -e "\e[1;33m"
    $DOCKER image build $PATH -t $IMAGETAG --platform=${PLATFORM} -f ${PATH}/${DOCKERFILE}
    echo -e "\e[33;0m"
}

banner(){
    ${ECHO} "** BSImage (build&scan image)"
    ${ECHO} "** build image and scan with trivy opensource"
}

scan(){

    if [ ! -d "$DIRLOG" ]; then
        $DIR $DIRLOG
    fi 
    
    echo $'\342\217\261' " Scanning..."
    $TRIVY image --exit-code 1 ${IMAGETAG} >> log/${EVIDENCE}

    if [ $? == 0 ]
    then
        ${ECHO} -e "\e[1;32mApproved! :)"
    else
        ${ECHO} -e $'\360\237\222\243' "\e[1;31m Not approved! :("
    fi
    ${ECHO} -e "\e[33;0mYou can check this evidence logfile: log/${EVIDENCE}"

}

case "$1" in
    "start")
        banner
        echo $'\360\237\222\273' "Starting..."
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