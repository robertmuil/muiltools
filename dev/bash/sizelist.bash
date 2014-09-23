function stripSize {
	echo $1
}

while read line; do
	echo `stripSize $line`
done
