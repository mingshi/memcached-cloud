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
    file="${orig_dir}/tarbal/memcached-1.4.0.tar.gz"
    cdir="memcached-1.4.0"
elif [ ${4} -eq "2" ]
then
    file="${orig_dir}/tarbal/memcached-1.4.4.tar.gz"
    cdir="memcached-1.4.4"
elif [ ${4} -eq "3" ]
then
    file="${orig_dir}/tarbal/memcached-1.4.13.tar.gz"
    cdir="memcached-1.4.13"
fi

##检查tarbal文件是否存在##
if [ ! -f ${file} ]
then
    echo "no the version tarbal file"
    exit
fi

##检查有无memcached目录##
is_memcached=`ssh -o StrictHostKeyChecking=no evans@${1} "find /home/www -maxdepth 1 -name memcached -type d"`
if [ -z "${is_memcached}" ]
then
    ssh -o StrictHostKeyChecking=no evans@${1} "mkdir -p /home/www/memcached"
fi

is_install=`ssh -o StrictHostKeyChecking=no evans@${1} "find /home/www/memcached -name '${cdir}' -type d"`
if [ -z "${is_install}" ]
then
    scp -q ${file} evans@${1}:/tmp/
    scp -q ${orig_dir}/tarbal/libevent-2.0.19-stable.tar.gz evans@${1}:/tmp/
    ssh -o StrictHostKeyChecking=no evans@${1} "cd /tmp/;tar xzf libevent-2.0.19-stable.tar.gz;cd libevent-2.0.19-stable;./configure --prefix=/home/www/libevent > /tmp/libconfig.log;make > /tmp/libmake.log;make install > /tmp/libinstall.log"
    libe=`ssh -o StrictHostKeyChecking=no evans@${1} "find /home/www/libevent -name lib -type d"`
    if [ -z "${libe}" ]
    then
        echo "remote host has no libevent"
        exit
    fi
    ssh -o StrictHostKeyChecking=no evans@${1} "cd /tmp/;tar xzf ${cdir}.tar.gz;cd ${cdir};./configure --prefix=/home/www/memcached/${cdir} --enable-64bit --with-libevent=/home/www/libevent > /tmp/${cdir}_config_log;make >/tmp/${cdir}_make_log;make install > /tmp/${cdir}_make_install_log"
    is_install_still=`ssh -o StrictHostKeyChecking=no evans@${1} "find /home/www/memcached -name '${cdir}' -type d"`
    if [ -z "${is_install_still}" ]
    then
        echo "the version isn't installed success!"
        exit
    fi
fi

##检查是否已经在运行##
check_first=`ssh -o StrictHostKeyChecking=no evans@${1} "ps -ef|grep memcached|awk '\\$2 != ${2}'|grep ${2}|grep -v grep|head -1|awk '{print \\$1}'"`
if [ ! -z "${check_first}" ]
then
    echo "is already running"
    exit
fi

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
    echo "start failed"
    exit
else
    echo "start success"
    exit
fi
