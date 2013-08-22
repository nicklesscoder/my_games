declare -a types=('c' 's' 'h' 'd')
for i in {0..51}
do
	orgfile=$((i+1)).png
	echo $orgfile
	num=$((i%4))
	type=${types[${num}]}
	val=$((i/4))
	if [ $val -eq 0 ]
	then
		val=A
	else 
		val=$((14-val))
	fi
	newfile=$val$type.png
	echo $orgfile : $type : $newfile
	mv $orgfile $newfile
done
