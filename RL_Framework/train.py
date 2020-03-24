import argparse
from dataset import Dataset
from net import Net
from trainer import Trainer
from constants import TrainingConstants, DeviceConstants
import torch.multiprocessing as mp
import os

if __name__ == '__main__':
    # Parse args.
    parser = argparse.ArgumentParser(description='Train a baseline network.')
    parser.add_argument(
        '--data_dir',
        type=str,
        help='Path to the training data.'
    )
    parser.add_argument(
        '--val_dir',
        type=str,
        help='Path to the validation data.'
    )
    parser.add_argument(
        '--num_epochs',
        type=int,
        default=TrainingConstants.NUM_EPOCHS,
        help='Number of training epochs.'
    )
    parser.add_argument(
        '--total_size',
        type=float,
        default=TrainingConstants.TOTAL_SIZE,
        help='The proportion of the data to use.'
    )
    parser.add_argument(
        '--val_size',
        type=float,
        default=TrainingConstants.VAL_SIZE,
        help='The proportion of the data to use for validation.'
    )
    parser.add_argument(
        '--bsz',
        type=int,
        default=TrainingConstants.BSZ,
        help='Training batch size.'
    )
    parser.add_argument(
        '--base_lr',
        type=float,
        default=TrainingConstants.BASE_LR,
        help='Base learning rate.'
    )
    parser.add_argument(
        '--lr_step_size',
        type=int,
        default=TrainingConstants.LR_STEP_SIZE,
        help='Step size for learning rate in epochs.'
    )
    parser.add_argument(
        '--lr_decay_rate',
        type=float,
        default=TrainingConstants.LR_DECAY_RATE,
        help='Decay rate for learning rate at every --lr_step_size.'
    )
    parser.add_argument(
        '--log_interval',
        type=int,
        default=TrainingConstants.LOG_INTERVAL,
        help='Log interval in batches.'
    )
    parser.add_argument(
        '--cuda',
        action='store_true',
        help='Enable CUDA support and utilize GPU devices.'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        default=TrainingConstants.OUTPUT_DIR,
        help='Directory to output logs and trained model to.'
    )
    parser.add_argument(
        '--net_name',
        type=str,
        default=TrainingConstants.NET_NAME,
        help='Name of network.'
    )
    parser.add_argument(
        '--nodes',
        default=1,
        type=int
    )
    parser.add_argument(
        '--gpus',
        default=1,
        type=int,
        help='number of GPUs per node'
    )
    parser.add_argument(
        '--nr',
        default=0,
        type=int,
        help='ranking within the nodes'
    )

    args = parser.parse_args()
    data_dir = args.data_dir
    val_dir = args.val_dir
    num_epochs = args.num_epochs
    total_size = args.total_size
    val_size = args.val_size
    bsz = args.bsz
    base_lr = args.base_lr
    lr_step_size = args.lr_step_size
    lr_decay_rate = args.lr_decay_rate
    log_interval = args.log_interval
    output_dir = args.output_dir
    net_name = args.net_name

    cuda = args.cuda
    if cuda:
        device = DeviceConstants.CUDA
    else:
        device = DeviceConstants.CPU

    train_dataset = Dataset(data_dir)
    val_dataset = Dataset(val_dir)
    net = Net(val_dataset.input_cc_mean, val_dataset.input_cc_std, val_dataset.input_raw_mean, val_dataset.input_raw_std, name=net_name)
    trainer = Trainer(net,
                      train_dataset,
                      val_dataset,
                      num_epochs,
                      total_size,
                      val_size,
                      bsz,
                      base_lr,
                      lr_step_size,
                      lr_decay_rate,
                      log_interval,
                      device,
                      output_dir)

    args.world_size = args.gpus * args.nodes
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'
    mp.spawn(trainer.train, nprocs=args.gpus, args=(args,))
    # trainer.train()