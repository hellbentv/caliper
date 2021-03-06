#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   wuyanjun 00291783
#   E-mail  :   wu.wu@hisilicon.com
#   Date    :   15/01/19 16:20:17
#   Desc    :  
#

import re
import string
import pdb

def iperf_parser(content, outfp, tag):
    score = -1
    sum_score = 0
    count = 0
    for speed in re.findall("MBytes(.*?)Mbits/sec", content):
        sum_score = string.atof( speed.strip() ) + sum_score
        count = count + 1
    if count != 0:
        score = sum_score / count
        outfp.write("speed of %s is %.3f Mbits/sec\n" % (tag, score))
    return score

def iperf_TCP_parser(content, outfp):
    return iperf_parser(content, outfp, 'iperf TCP')

def iperf_UDP_parser(content, outfp):
    return iperf_parser(content, outfp, 'iperf UDP')

if __name__=="__main__":
    infp = open("1.txt", "r")
    content = infp.read()
    outfp = open("2.txt", "a+")
    pdb.set_trace()
    iperf_TCP_parser(content, outfp)

    iperf_UDP_parser(content, outfp)
    outfp.close()
    infp.close()
