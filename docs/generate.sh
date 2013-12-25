for i in *.ipynb
do
if ! ( echo $i | grep -q "^$test" ) 
# if the file does not begin with $pattern rename it.
then runipy $i --to rst
fi
done