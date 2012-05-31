#!/bin/bash
orig_dir=$(pwd)
#检查是否需要随安装启动##
if [ "${5}" -eq 1 ]
then
    #检查ip是否存在##
    if [ -z "${1}" ]
    then
        echo "no ip inputed"
        exit
    fi
    
    ##检查版本是否选择##
    if [ -z "${2}" ]
    then
        echo "no version selected"
        exit
    fi
    
    ##检查启动参数是否设置##
    if [ -z "${3}" ]
    then
        echo "no port inputed"
        exit
    fi
    
    ##检查memory是否输入##
    if [ -z "${4}" ]
    then
        echo "no memory inputed"
        exit
    fi
    
    ##设置文件和路径等##
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
    
    ##检查tarbal文件是否存在##
    if [ ! -f ${file} ]
    then
        echo "no the version tarbal file"
        exit
    fi
    
    ##检查网络状况##
    result=`nmap -sT ${1} -p 22 | grep open|awk '{print $1}'`
    if [ -z "${result}" ]
    then
        echo "can't connect to the ip address"
        exit
    fi
   
    ##检查有无memcached目录##
    is_memcached=`ssh evans@${1} "find /home/www -name memcached -type d"`
    if [ -z "${is_memcached}" ]
    then
        ssh evans@${1} "mkdir -p /home/www/memcached"
    fi

    ##检查该服务器是否已经安装相应版本##
    is_install=`ssh evans@${1} "find /home/www/memcached -name '${cdir}' -type d"`
    if [ -z "${is_install}" ]
    then
        scp -q ${file} evans@${1}:/tmp/
        ##检查libevent是否安装##
        libe=`ssh evans@${1} "ls -la /usr/lib64|grep 'libevent'|grep 'core'|head -1"|awk '{print $1}'`
        if [ -z "${libe}" ]
        then
            echo "remote host has no libevent"
            exit
        fi
        ssh evans@${1} "cd /tmp/;tar xzf ${cdir}.tar.gz;cd ${cdir};./configure --prefix=/home/www/memcached/${cdir} --enable-64bit > /tmp/${cdir}_config_log;make >/tmp/${cdir}_make_log;make install > /tmp/${cdir}_make_install_log"
    fi
    
    
    ##检查是否端口已经存在##
    thisport=${3}
    port=`ssh evans@${1} "ps -ef|grep memcached|awk '\\$2 != ${thisport}'|grep ${thisport}|grep -v grep |head -1|awk '{print \\$1}'"`
    if [ ! -z "${port}" ]
    then
        echo "port has in used"
        exit
    fi
    
    if [ ! -z "${6}" ]
    then 
        ssh evans@${1} "/home/www/memcached/${cdir}/bin/memcached -p ${3} -m ${4} ${6} -d"
    else
        ssh evans@${1} "/home/www/memcached/${cdir}/bin/memcached -p ${3} -m ${4} -d"
    fi
    
    
    ##检查运行是否正常##
    check=`ssh evans@${1} "ps -ef|grep memcached|awk '\\$2 != ${thisport}'|grep ${thisport}|grep -v grep|head -1|awk '{print \\$1}'"`
    if [ -z "${check}" ]
    then
        echo "add failed"
        exit
    else
        echo "add success"
        exit
    fi
else
    echo "no start"
    exit
fi
