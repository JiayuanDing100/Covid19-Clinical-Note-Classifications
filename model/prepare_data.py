from __future__ import absolute_import, division, print_function
import pandas as pd
import csv
import os
import sys
import logging

logger = logging.getLogger()
csv.field_size_limit(2147483647) # Increase CSV reader's field limit incase we have long text.


def prepare_data():
    train_df = pd.read_csv('../data/train.csv', header=None, error_bad_lines=False)
    print(train_df.head())

    test_df = pd.read_csv('../data/test.csv', header=None, error_bad_lines=False)
    print(test_df.head())


    print(train_df[0])
    train_df[0] = (train_df[0] == 1).astype(int)
    test_df[0] = (test_df[0] == 1).astype(int)
    print(train_df.head())
    # ------------------------------form data-----
    train_df_bert = pd.DataFrame({
        'id':range(len(train_df)),
        'label':train_df[0],
        'alpha':['a']*train_df.shape[0],
        'text': train_df[1].replace(r'\n', ' ', regex=True)
    })
    print(train_df_bert.head())
    dev_df_bert = pd.DataFrame({
        'id':range(len(test_df)),
        'label':test_df[0],
        'alpha':['a']*test_df.shape[0],
        'text': test_df[1].replace(r'\n', ' ', regex=True)
    })
    print(dev_df_bert.head())
    train_df_bert.to_csv('../data/train.tsv', sep='\t', index=False, header=False)
    dev_df_bert.to_csv('../data/dev.tsv', sep='\t', index=False, header=False)


prepare_data()