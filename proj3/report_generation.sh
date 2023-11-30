rm ./output/PODEM_test_vectors.txt

INFILE=s27.txt
list='16sa0 10sa1 12sa0 18sa1 17sa1 13sa0 6sa1 11sa0'
# '
for FAULT in $list; do
    python3 ./proj3_deyuan.py $INFILE $FAULT >> ./output/PODEM_test_vectors.txt
done

INFILE=s298f_2.txt
list='70sa1 73sa0 26sa1 92sa0 38sa0 46sa1 3sa1 68sa0'

for FAULT in $list; do
    python3 ./proj3_deyuan.py $INFILE $FAULT >> ./output/PODEM_test_vectors.txt
done

INFILE=s344f_2.txt
list='166sa0 71sa1 16sa0 91sa1 38sa0 5sa1 138sa0 91sa0'

for FAULT in $list; do
    python3 ./proj3_deyuan.py $INFILE $FAULT >> ./output/PODEM_test_vectors.txt
done

INFILE=s349f_2.txt
list='25sa1 51sa0 105sa1 105sa0 83sa1 92sa0 7sa0 179sa0'

for FAULT in $list; do
    python3 ./proj3_deyuan.py $INFILE $FAULT >> ./output/PODEM_test_vectors.txt
done