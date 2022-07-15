#! /bin/bash
#
# run.sh -- build and optionally test the software in this repo via docker
#
# type "run.sh -h" to see detailed help
#
prog=$(basename $0)
execdir=$(dirname $0)
[ "$execdir" = "" -o "$execdir" = "." ] && execdir=$PWD
export CODEDIR=$( (
    cd $execdir/.. >/dev/null 2>&1
    pwd
))
export DOCKERDIR=$CODEDIR/docker

export PACKAGE_NAME=oar-filemanager

echo '+' docker build $BUILD_OPTS -t $PACKAGE_NAME/fm -f $DOCKERDIR/Dockerfile $CODEDIR
docker build $BUILD_OPTS -t $PACKAGE_NAME/fm -f $DOCKERDIR/Dockerfile $CODEDIR
