for i in {1..5}
do
	cd $i
	ln -s WANNIERS-HOMO_centers_s1-1.data wanniers
	cd ..
done

