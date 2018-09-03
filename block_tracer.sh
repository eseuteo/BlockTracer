# Recibe path ($1)
# Recibe lista especies ($2)

species_a=$(head -n 1 $2)
for species in $(tail -n +2 $2); do
    species_b=$species
    comparisons_list=$(ls $species_a*$species_b*.csv)
    hacer_algo_con_lista_comp
    species_a=$species
done