
file_id=1
for file1 in $( find `pwd` -type f -regex '.*/HUMAN-CHR.+_PONAB.*' ); do
    chromosome_PONAB=$(echo $file1 | sed -r 's/.*PONAB-CHR(.+)\..*/\1/g')
    for file2 in $(find `pwd` -type f -regex '.*/PONAB-CHR'$chromosome_PONAB'_MOUSE.*'); do
        chromosome_MOUSE=$(echo $file2 | sed -r 's/.*MOUSE-CHR(.+)\..*/\1/g')
        for file3 in $(find `pwd` -type f -regex '.*/MOUSE-CHR'$chromosome_MOUSE'_HORSE.*'); do
            chromosome_HORSE=$(echo $file3 | sed -r 's/.*HORSE-CHR(.+)\..*/\1/g')
            for file4 in $(find `pwd` -type f -regex '.*/HORSE-CHR'$chromosome_HORSE'_BOSTA.*'); do
                echo $file1 > ../input_files/input_file-$file_id.txt
                echo $file2 >> ../input_files/input_file-$file_id.txt
                echo $file3 >> ../input_files/input_file-$file_id.txt
                echo $file4 >> ../input_files/input_file-$file_id.txt
                ((file_id++))
            done
        done
    done
done