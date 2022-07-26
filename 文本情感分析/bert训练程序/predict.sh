python run_test.py \
  --task_name=senti \
  --do_predict=true \
  --data_dir=data_set \
  --vocab_file=chinese_L-12_H-768_A-12/vocab.txt \
  --bert_config_file=chinese_L-12_H-768_A-12/bert_config.json \
  --init_checkpoint=senti_model_test\
  --max_seq_length=165 \
  --output_dir=senti_predict_test2
exec /bin/bash

