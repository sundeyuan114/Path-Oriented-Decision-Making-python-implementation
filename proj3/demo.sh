echo ""
echo "!!!this script only works in MAC and LINUX, no WINDOWS!!!"
echo ""
echo "type the exact input file name (i.e., s27.txt)"
read INFILE
echo "type the exact fault net + "sa" + stuck at value (i.e., 23sa0)"
read FAULT


echo "rm all the previous generated files"
rm ./output/PODEM_test_vectors.txt
rm ./files/input_vectors.txt
rm ./output/fault_detected.txt
#Use my PODEM code to generate a general test vector
python3 ./proj3_deyuan.py $INFILE $FAULT > ./output/PODEM_test_vectors.txt
echo "PODEM is DONE"
#generate all possible vectors of given PODEM TEST
python3 input_vector_generatior.py ./output/PODEM_test_vectors.txt > ./files/input_vectors.txt
echo "Generating all possible test vectors"
#Test each of the PODEM vector
python3 ./proj2_deyuan.py $INFILE input_vectors.txt > ./output/fault_detected.txt
echo "Check all faults detected in fault_detected.txt"
