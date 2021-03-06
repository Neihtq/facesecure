import os
import numpy as np
import matplotlib.pyplot as plt

from pytorch_lightning import Callback

from face_recognition.utils.constants import RESULTS_DIR


class MetricsCallback(Callback):
    def __init__(self):
        super().__init__()
        self.val_loss = []
        self.loss = []
        self.val_acc = []
        self.acc = []
        self.fp_rate = []
        self.tp_rate = []
        self.roc_auc = []

    def on_validation_epoch_end(self, trainer, pl_module):
        metrics = trainer.logged_metrics
        if 'val_loss' in metrics:            
            self.val_loss.append(float(metrics['val_loss']))
            self.val_acc.append(float(metrics["val_acc"]))

    def on_epoch_end(self, trainer, pl_module):
        metrics = trainer.logged_metrics
        if 'train_loss' in metrics:
            self.loss.append(metrics['train_loss'])

    def on_test_end(self, trainer, pl_module):
        metrics = trainer.logged_metrics
        acc = metrics["test_acc"]
        print(acc)

    def on_fit_end(self, trainer, pl_module):
        self.plot_accuracy()
        self.plot_loss()

    def plot_loss(self):
        train_loss = self.loss
        val_loss = self.val_loss
        fig = plt.figure()
        epochs = len(train_loss)
        if epochs < len(val_loss):
            start = len(val_loss) - epochs
            val_loss = val_loss[start:]
        
        plt.plot(range(epochs), train_loss, color='red', label='Train Loss on VGG')
        plt.plot(range(epochs), val_loss, color='blue', label='Val Loss on VGG')
        plt.ylim(bottom=0)
        plt.title('Loss curve on VGG')
        plt.legend(loc='upper right')
        fig.savefig(os.path.join(RESULTS_DIR, "losses.png"), dpi=fig.dpi)
        plt.show()

    def plot_accuracy(self):
        accuracy_list = self.val_acc
        epochs = len(self.val_acc)
        fig = plt.figure()
        plt.plot(range(epochs), accuracy_list, color='red', label='LFW Accuracy')
        plt.ylim([0.0, 1.05])
        plt.xlim([0, epochs + 1])
        plt.xlabel('Epoch')
        plt.ylabel('LFW Accuracy')
        plt.title('Evaluation Accuracy on LFW')
        plt.legend(loc='lower right')
        fig.savefig(os.path.join(RESULTS_DIR, "lfw_eval_accuracies.png"), dpi=fig.dpi)
        plt.show()
        