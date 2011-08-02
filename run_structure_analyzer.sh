run () {
	echo "Going to do run #$1 using analysis $2"
	cd $1
	structure-analyzer 1 $2
	cd ..
}

for i in `seq $1 $2`
do
	run $i $3 > /dev/null &
done
