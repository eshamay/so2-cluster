fix() {
	cd $1
	rm -f wanniers xyz system.cfg h2o_polarizability.dat
	ln -s ../../system.cfg .
	ln -s WANNIER* wanniers
	ln -s *pos*xyz xyz
	ln -s ~/md/Arcade/sfg/h2o_polarizability.dat .
	cd ..
}

for i in `seq 1 10`
do
	fix $i
done
