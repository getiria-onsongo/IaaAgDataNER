# page level (standard)
mkdir jul20_pg_level
cd jul20_pg_level
nohup python ~/packages/IaaAgDataNER/src/cross_validation.py ~/packages/IaaAgDataNER/Data/DavisLJ11 --pos &
wait $!
cd ..

# glove word embeddings
mkdir jul20_pg_level_word_embed
cd jul20_pg_level_word_embed
nohup python ~/packages/IaaAgDataNER/src/cross_validation.py ~/packages/IaaAgDataNER/Data/DavisLJ11 --word_embed --vectors ~/packages/IaaAgDataNER/glove.6B.zip &
wait $!
cd ..

# GPU
mkdir jul20_pg_level_gpu
cd jul20_pg_level_gpu
nohup python ~/packages/IaaAgDataNER/src/cross_validation.py ~/packages/IaaAgDataNER/Data/DavisLJ11 --GPU &
wait $!
cd ..

# GPU
mkdir jul20_pg_level_spancat
cd jul20_pg_level_spancat
nohup python ~/packages/IaaAgDataNER/src/cross_validation.py ~/packages/IaaAgDataNER/Data/DavisLJ11 --spancat &
wait $!
cd ..
