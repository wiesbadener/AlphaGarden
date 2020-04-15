from setuptools import setup
import os
import sys
setup(
    name = "alphagarden",
    version = "0.0.1",
    python_requires = '==3.7.7',
    packages=[ 
        'simalphagarden', 
        'wrapperenv', 
        'simulator'],
    package_dir={'simalphagarden': 'alphagarden/Learning', 
        'wrapperenv': 'alphagarden/Learning', 
        'simulator': 'alphagarden/Simulator'},
    install_requires = [ 
        "absl-py==0.9.0",
        "astor==0.8.1",
        "atari-py==0.2.6",
        "cloudpickle==1.2.2",
        "cycler==0.10.0",
        "Deprecated==1.2.7",
        "future==0.18.2",
        "gast==0.2.2",
        "google-pasta==0.1.8",
        "grpcio==1.27.2",
        "gym==0.16.0",
        "h5py==2.10.0",
        "joblib==0.14.1",
        "Keras-Applications==1.0.8",
        "Keras-Preprocessing==1.1.0",
        "kiwisolver==1.1.0",
        "Markdown==3.2.1",
        "matplotlib==3.1.3",
        "numpy==1.18.1",
        "opencv-python==4.2.0.32",
        "opt-einsum==3.1.0",
        "pandas==1.0.1",
        "Pillow==7.0.0",
        "protobuf==3.11.3",
        "pyglet==1.5.0",
        "pyparsing==2.4.6",
        "python-dateutil==2.8.1",
        "pytz==2019.3",
        "scipy==1.4.1",
        "six==1.14.0",
        "stable-baselines==2.9.0",
        "tensorboard==1.15.0",
        "tensorflow==1.15.0",
        "tensorflow-estimator==1.15.1",
        "termcolor==1.1.0",
        "Werkzeug==1.0.0",
        "wrapt==1.12.0",
        ] + [] if "win" in sys.platform else ["torch==1.4.0"],
)