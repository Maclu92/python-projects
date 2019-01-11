#!/bin/bash

# definition of MAC addresses
monster=$(echo $MONSTER)

echo "Which PC to wake?"
echo "m) homeWarden"
echo "q) quit"
read input1
case $input1 in
  m)
    /usr/bin/wol $monster
    exit
    ;;
  g)
    # uses wol over the internet provided that port 9 is forwarded to ghost on ghost's router
    #/usr/bin/wol --port=9 --host=ghost.mydomain.org $ghost
    ;;
  Q|q)
      clear	  
      exit
    ;;
esac
