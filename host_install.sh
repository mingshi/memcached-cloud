#!/bin/bash
orig_dir=$(pwd)
#检查ip是否存在##
if [ -z "${1}" ]
then
    echo "no ip address"
    exit
fi

##检查版本是否选择##
if [ -z "${2}" ]
then
    echo "no version selected"
    exit
fi

if [ ${2} -eq "1" ]
then
    file="${orig_dir}/tarbal/memcached-1.4.0.tar.gz"
    cdir="memcached-1.4.0"
elif [ ${2} -eq "2" ]
then
    file="${orig_dir}/tarbal/memcached-1.4.4.tar.gz"
    cdir="memcached-1.4.4"
elif [ ${2} -eq "3" ]
then
    file="${orig_dir}/tarbal/memcached-1.4.13.tar.gz"
    cdir="memcached-1.4.13"
fi

##检查文件是否存在##
if [ ! -f ${file} ]
then
    echo "no the version tarbal file"
    exit
fi
##检查是否可以上传文件##
result=`nmap -sT ${1} -p 22 | grep open|awk '{print $1}'`
if [ -z "${result}" ]
then
    echo "can't connect to the ip address"
    exit
else
    scp -q ${file} evans@${1}:/tmp/
fi

##检查libevent是否安装##
libe=`ssh evans@${1} "ls -la /usr/lib|grep 'libevent'|grep 'core'|head -1"|awk '{print $1}'`
if [ -z "${libe}" ]
then
    echo "remote host has no libevent"
    exit
fi

##进行解压编译安装##
ssh evans@${1} "cd /tmp/;tar xzf ${cdir}.tar.gz;cd ${cdir};./configure --prefix=/home/evans > /home/evans/config_log;make >/home/evans/make_log;make install > make_install_log"

##检查安装是否正常##
check=`ssh evans@${1} "/home/evans/bin/memcached -help|head -1"|awk '{print $1}'`
if [ "${check}" != "memcached" ]
then
    echo "install failed"
    exit
else
    echo "install success!"
    exit
fi
