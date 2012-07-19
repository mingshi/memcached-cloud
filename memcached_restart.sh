#!/bin/bash
orig_dir=$(cd "$(dirname "$0")"; pwd)
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

is_install=`ssh -o StrictHostKeyChecking=no evans@${1} "find /home/www/memcached -name '${cdir}' -type d"`
if [ -z "${is_install}" ]
then
    echo "this version didn't install"
    exit
fi

pid=`ssh -o StrictHostKeyChecking=no evans@${1} "ps -ef|grep memcached|awk '\\$2 != ${2}'|grep ${2}|grep -v grep |head -1|awk '{print \\$2}'"`
ssh -o StrictHostKeyChecking=no evans@${1} "kill ${pid} 2>/dev/null"

##检查参数并启动##
if [ ! -z "${5}" ]
then
    ssh -o StrictHostKeyChecking=no evans@${1} "/home/www/memcached/${cdir}/bin/memcached -p ${2} -m ${3} ${5} -d"
else
    ssh -o StrictHostKeyChecking=no evans@${1} "/home/www/memcached/${cdir}/bin/memcached -p ${2} -m ${3} -d"
fi

##检查是否启动成功##
check=`ssh -o StrictHostKeyChecking=no evans@${1} "ps -ef|grep memcached|awk '\\$2 != ${2}'|grep ${2}|grep -v grep|head -1|awk '{print \\$1}'"`
if [ -z "${check}" ]
then
    echo "restart failed"
    exit
else
    echo "restart success"
    exit
fi
