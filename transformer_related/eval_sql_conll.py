
import logging
import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np
from seqeval.metrics import f1_score, precision_score, recall_score

logger = logging.getLogger(__name__)


def compute_metrics(preds_list, out_label_list) -> Dict:
    return {
        "precision": precision_score(out_label_list, preds_list),
        "recall": recall_score(out_label_list, preds_list),
        "f1": f1_score(out_label_list, preds_list),
    }

if __name__ == "__main__":
    pred_content = open(sys.argv[1], "r").read().rstrip().split("\n\n")
    out_content = open(sys.argv[2], "r").read().rstrip().split("\n\n")
    assert len(pred_content) == len(out_content)
    print(len(pred_content), len(out_content))
    #print(pred_content[0][:10], out_content[0][:10])
    #print(list(zip(pred_content[0], out_content[0])))

    #sys.exit(0)
    preds_list = []
    out_label_list = []
    for sentid, (pred_sent, out_sent) in enumerate(zip(pred_content, out_content)):
        #print(sentid, pred_sent.split("\n"))
        pred_arr = [item.split(" ")[1] for item in pred_sent.split("\n")]
        out_arr = [item.split(" ")[1] for item in out_sent.split("\n")][:len(pred_arr)]
        preds_list.extend(pred_arr)
        out_label_list.extend(out_arr)
        #break
    assert len(preds_list) == len(out_label_list)
    print(compute_metrics(preds_list, out_label_list))
    preds_list = [item[:2]+"Event" if item!="O" else item for item in preds_list]
    out_label_list = [item[:2]+"Event" if item!="O" else item for item in out_label_list]
    print(compute_metrics(preds_list, out_label_list))
