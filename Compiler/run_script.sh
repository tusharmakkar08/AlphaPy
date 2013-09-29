#/bin/bash
obj_file=$1
cont=1
echo "Started"
echo "Press ENTER to exit"
while [ $cont -eq "1" ]
do
read -s -n 1 in
if [ "$in" = "" ];
then
cont=0
exit
fi
done
	
