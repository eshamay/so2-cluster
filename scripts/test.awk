BEGIN {
	state = 0;
}

{
	count[state, $1] = count[state, $1] + 1;
	state = $1
}

END {
	for (x in count) {
		print x, "--", count[x]
	}

}
