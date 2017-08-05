#!/bin/bash
if [[ "$1" == "on" ]] ; then
  echo "in if"
  pigs pwm 23 0 pwm 24 0 pwm 25 0
else
  echo "in else"
  if [[ "$1" == "off" ]] ; then
    echo "in else"
    pigs pwm 23 255 pwm 24 255 pwm 25 255
  else
    echo "hello"
    # trying to compensate for eye's log response to brightness
#   tmpR=`echo 'scale=4; (e(l(2) * (((100 - '$1') * 8) / 100))-0.01)' | bc -l`
#   tmpG=`echo 'scale=4; (e(l(2) * (((100 - '$2') * 8) / 100))-0.01)' | bc -l`
#   tmpB=`echo 'scale=4; (e(l(2) * (((100 - '$3') * 8) / 100))-0.01)' | bc -l`

    # but simple linear seems to work better :-(
    tmpR=`echo 'scale=4; ((100-'$1')*255/100)' | bc -l`
    tmpG=`echo 'scale=4; ((100-'$2')*255/100)' | bc -l`
    tmpB=`echo 'scale=4; ((100-'$3')*255/100)' | bc -l`

    # convert to integer
    tmpR=`echo 'scale=0; ('$tmpR'/1)' | bc -l`
    tmpG=`echo 'scale=0; ('$tmpG'/1)' | bc -l`
    tmpB=`echo 'scale=0; ('$tmpB'/1)' | bc -l`

    # echo "RGB: "$tmpR $tmpG $tmpB
    pigs pwm 15 $tmpR pwm 18 $tmpG pwm 14 $tmpB
  fi
fi
