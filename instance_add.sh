#!/bin/bash
orig_dir=$(pwd)
#检查ip是否存在##
if [ -z "${1}" ]
then
    echo "no ip selected"
    exit
fi

##检查启动参数是否设置##
if [ -z "${2}" ]
then
    echo "no params inputed"
    exit
fi

##检查是否端口已经存在##
thisport=`echo ${2}|awk -F p '{print $2}'|awk '{print $1}'`
port=`ssh evans@${1} "ps -ef|grep memcached|awk '\\$2 != ${thisport}'|grep ${thisport}|grep -v grep |head -1|awk '{print \\$1}'"`
if [ ! -z "${port}" ]
then
    echo "port has in used"
    exit
fi

##检查是否可以连接启动##
result=`nmap -sT ${1} -p 22 | grep open|awk '{print $1}'`
if [ -z "${result}" ]
then
    echo "can't connect to the ip address"
    exit
else
    ssh evans@${1} "/home/evans/bin/memcached ${2}"
fi


##检查运行是否正常##
check=`ssh evans@${1} "ps -ef|grep memcached|awk '\\$2 != ${thisport}'|grep ${thisport}|grep -v grep|head -1|awk '{print \\$1}'"`
if [ -z "${check}" ]
then
    echo "add failed"
    exit
else
    echo "add success!"
    exit
fi
