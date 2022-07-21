# standard
mkdir jul21_pg_level
cd jul21_pg_level
nohup python3 ~/packages/IaaAgDataNER/src/cross_validation.py ~/data/dev_onsongo_Jul21 --pos
cd ..

# glove word embeddings
mkdir jul21_pg_level_word_embed
cd jul21_pg_level_word_embed
nohup python3 ~/packages/IaaAgDataNER/src/cross_validation.py ~/data/dev_onsongo_Jul21 --pos --word_embed --vectors ~/packages/IaaAgDataNER/glove.6B.zip
cd ..

# GPU
mkdir jul21_pg_level_gpu
cd jul21_pg_level_gpu
nohup python3 ~/packages/IaaAgDataNER/src/cross_validation.py ~/data/dev_onsongo_Jul21 --pos --GPU
cd ..
