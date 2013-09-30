#/bin/bash
cont=1
i=0
args_file=$1

while read line; do
	var[$i]=$line
	i=$(( i + 1 ))
done < $args_file

#~ echo ${var[2]}

case ${var[1]} in
	"c") "${var[0]}" "${var[2]}" ; ret=$? ;;
	"cpp") "${var[0]}" "${var[2]}" ; ret=$? ;;
	"java") echo "Execution of Java programs is currently unsupported" ;;
	"py") python "${var[0]}" "${var[2]}"; ret=$? ;;
	"sh") sh "${var[0]}" "${var[2]}"; ret=$? ;;
	"rb") ruby "${var[0]}" "${var[2]}"; ret=$? ;;
	"R") R CMD BATCH "${var[0]}" "${var[2]}"; ret=$? ;;
	*) echo "Language unsopperted by the editor";;
esac
echo "-----------------------------------------------------------------"
echo "Program exited with return code : $ret"
echo "Press ENTER to exit"
while [ $cont -eq "1" ]; do
	read -s -n 1 in
	if [ "$in" = "" ]; then
		cont=0
	fi
done
	
