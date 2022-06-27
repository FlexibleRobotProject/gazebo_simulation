#!/usr/bin/env python
# coding=utf-8
# women renwei, zhe shi yige log wenjian 
import inspect
import os
import random
import sys
def extract_log(log_file,new_log_file,key_word):
    with open(log_file, 'r') as f:  # ,encoding='utf-16LE'
      with open(new_log_file, 'w') as train_log:
  #f = open(log_file)
    #train_log = open(new_log_file, 'w')
        for line in f:
    # qu chu duo gpu de tong bu log
          if 'Syncing' in line:
            continue
    # qu chu chu ling cuo wu de log
          if 'nan' in line:
            continue
          if key_word in line:
            print("keyword get!")
            train_log.write(line)
    f.close()
    train_log.close()
 
extract_log('person_train_log.txt','train_log_loss.txt','images')
extract_log('person_train_log.txt','train_log_iou.txt','IOU')
extract_log('person_train_log.txt','train_log_map.txt','mAP@0.50') 
extract_log('person_train_log.txt','train_log_F1.txt','F1-score')
