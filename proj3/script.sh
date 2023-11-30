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
echo "PODEM is DONE, check PODEM_test_vector.txt for generated podem test vector"
#generate all possible vectors of given PODEM TEST
python3 input_vector_generatior.py ./output/PODEM_test_vectors.txt > ./files/input_vectors.txt
echo "generate all possible test vectors according based on PODEM result, (This might take long, like 60 seconds?)"
#Test each of the PODEM vector
python3 ./proj2_deyuan.py $INFILE input_vectors.txt > ./output/fault_detected.txt
echo "check all the output in fault_detected.txt , search for the fault, and there should be 2**count("X") numbers of fault appears"