# page level (standard)
mkdir jul19_pg_level
cd jul19_pg_level
nohup python ~/packages/IaaAgDataNER/src/cross_validation.py ~/packages/IaaAgDataNER/Data/page_level &
cd ..

# sentence level
mkdir jul19_sent_level
cd jul19_sent_level
nohup python ~/packages/IaaAgDataNER/src/cross_validation.py ~/packages/IaaAgDataNER/Data/sentence_level --sent_level &
cd ..

# page level glove pretrained word embeddings
mkdir jul19_pg_level_word_embed
cd jul19_pg_level_word_embed
nohup python ~/packages/IaaAgDataNER/src/cross_validation.py ~/packages/IaaAgDataNER/Data/page_level --word_embed --vectors ~/packages/IaaAgDataNER/glove.6B.zip &
cd ..

# page level gpu / spacy transformers
mkdir jul19_pg_level_gpu
cd jul19_pg_level_gpu
nohup python ~/packages/IaaAgDataNER/src/cross_validation.py ~/packages/IaaAgDataNER/Data/page_level --GPU &
cd ..
