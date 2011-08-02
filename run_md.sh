# for the hot runs - 290K
#for i in {1..5}
#do
#	echo "Creating the input file for run $i - hot run"
#	# fix the title for the run
#	sed -i "s/PROJECT_NAME.*/PROJECT_NAME so2-cluster-md-$i/" md.inp
#  sed -i "s/RESTART_FILE_NAME.*/RESTART_FILE_NAME so2-cluster-md-$i-1.restart/" md.inp
#	# copy over the restart files
#  echo "Copying restart files"
#	cp ../init/$i/so2-cluster-init-$i-1.restart $i/so2-cluster-md-$i-1.restart
#  cp ../init/$i/so2-cluster-init-$i-RESTART.wfn $i/so2-cluster-md-$i-RESTART.wfn
#
#	# fix the temperature
#	sed -i "s/TEMPERATURE.*/TEMPERATURE 290.0/g" md.inp
#	cp md.inp $i/md.inp
#	sleep 3
#
#	# fix the pbs title
#	sed -i "s/PBS -N.*/PBS -N so2-cluster-md-$i/" pbs.so2
#
#	echo "Starting run $i"
#	# start the run
#	cd $i
#	qsub ../pbs.so2
#	sleep 3
#	cd ..
#done
#
# for the cold surface runs - 250K
for i in {6..10}
do
	echo "Creating the input file for run $i - cold run"
	# fix the title for the run
	sed -i "s/PROJECT_NAME.*/PROJECT_NAME so2-cluster-md-$i/" md.inp
  sed -i "s/RESTART_FILE_NAME.*/RESTART_FILE_NAME so2-cluster-md-$i-1.restart/" md.inp
	# copy over the restart files
  echo "Copying restart files"
	cp ../init/$i/so2-cluster-init-$i-1.restart $i/so2-cluster-md-$i-1.restart
  cp ../init/$i/so2-cluster-init-$i-RESTART.wfn $i/so2-cluster-md-$i-RESTART.wfn

	# fix the temperature
	sed -i "s/TEMPERATURE.*/TEMPERATURE 250.0/g" md.inp
	cp md.inp $i/md.inp
	sleep 3

	# fix the pbs title
	sed -i "s/PBS -N.*/PBS -N so2-cluster-md-$i/" pbs.so2

	echo "Starting run $i"
	# start the run
	cd $i
	qsub ../pbs.so2
	sleep 3
	cd ..
done
