python run_classifier.py \
  --task_name=sds \
  --do_predict=true \
  --data_dir=data_set \
  --vocab_file=chinese_L-12_H-768_A-12/vocab.txt \
  --bert_config_file=chinese_L-12_H-768_A-12/bert_config.json \
  --init_checkpoint=sds1_model\
  --max_seq_length=80\
  --output_dir=sds1_predict
exec /bin/bash

