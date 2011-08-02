function run_md {
	echo "Fixing the titles"
	# fix the title for the run
	sed -i "s/PBS -N.*/PBS -N so2-$2-md-$1/" pbs.restart
	sed -i "s/PROJECT_NAME.*/PROJECT_NAME so2-cluster-md-$1/" restart.inp
  sed -i "s/RESTART_FILE_NAME.*/RESTART_FILE_NAME so2-cluster-md-$1-1.restart/" restart.inp

	# fix the temperature
	sed -i "s/TEMPERATURE.*/TEMPERATURE $2/" restart.inp

	cp restart.inp $1/restart.inp

	# copy over the restart files from the init location
	cp ../init/$1/so2-cluster-init-$1-RESTART.wfn $1/so2-cluster-md-$1-RESTART.wfn
	cp ../init/$1/so2-cluster-init-$1-1.restart $1/so2-cluster-md-$1-1.restart

	sleep 2
	echo "Starting run $1"
	# start the run
	cd $1
	qsub ../pbs.restart
	cd ..
}

function run_restart {
	echo "Fixing the titles"
	# fix the title for the run
	sed -i "s/PBS -N.*/PBS -N so2-$2-md-$1/" pbs.restart
	sed -i "s/PROJECT_NAME.*/PROJECT_NAME so2-cluster-md-$1/" restart.inp
  sed -i "s/RESTART_FILE_NAME.*/RESTART_FILE_NAME so2-cluster-md-$1-1.restart/" restart.inp

	# fix the temperature
	sed -i "s/TEMPERATURE.*/TEMPERATURE $2/" restart.inp

	cp restart.inp $1/restart.inp

	sleep 2
	echo "Starting run $1"
	# start the run
	cd $1
	qsub ../pbs.restart
	cd ..
}

for i in `seq 9 10`
do 
	run_restart $i 290.0
done
