#!/bin/bash
orig_dir=$(pwd)
##检查ip是否存在##
if [ -z "${1}" ]
then
    echo "no ip inputed"
    exit
fi

##检查port是否存在##
if [ -z "${2}" ]
then
    echo "no port inputed"
    exit
fi

##检查内存是否设置##

if [ -z "${3}" ]
then
    echo "no memory inputed"
    exit
fi

##检查version是否存在##

if [ -z "${4}" ]
then
    echo "no version selected"
    exit
fi

##检查版本是否安装##
if [ ${4} -eq "1" ]
then
    cdir="memcached-1.4.0"
elif [ ${4} -eq "2" ]
then
    cdir="memcached-1.4.4"
elif [ ${4} -eq "3" ]
then
    cdir="memcached-1.4.13"
fi


##检查是否已经在运行##
check_first=`ssh evans@${1} "ps -ef|grep memcached|awk '\\$2 != ${2}'|grep ${2}|grep -v grep|head -1|awk '{print \\$1}'"`
if [ -z "${check_first}" ]
then
    echo "is already stop"
    exit
fi

##检查并stop##
pid=`ssh evans@${1} "ps -ef|grep memcached|awk '\\$2 != ${2}'|grep ${2}|grep -v grep|head -1|awk '{print \\$2}'"`
if [ ! -z ${pid} ]
then
    ssh evans@${1} "kill ${pid} 2>/dev/null"
else
    echo "no pid found"
fi

##检查是否stop成功##
check=`ssh evans@${1} "ps -ef|grep memcached|awk '\\$2 != ${2}'|grep ${2}|grep -v grep|head -1|awk '{print \\$1}'"`
if [ -z "${check}" ]
then
    echo "stop success"
    exit
else
    echo "stop failed"
    exit
fi
