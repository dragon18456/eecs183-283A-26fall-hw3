# Assignment 3: Sequence Modeling

**EECS 183 / 283A · Fall 2026 · 100 points + 10 bonus points**

Complete the TODOs and starred (★) questions in [hw3.ipynb](hw3.ipynb).
The assignment covers language-model sampling, n-gram and LSTM models,
sentiment classification, and sequence-to-sequence translation with attention.

## Run in Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dragon18456/eecs183-283A-26fall-hw3/blob/main/hw3.ipynb)

1. Open the notebook and choose **File → Save a copy in Drive**.
2. Under **Runtime → Change runtime type**, select runtime **2026.07**
   (Python 3.12) and a **T4 GPU** or another available GPU.
3. Run the setup cell. If it installs packages, follow its instruction to
   **Restart session**, then rerun setup. Allow the Google Drive mount.
4. Complete the TODOs and run the remaining cells in order.

The setup cell downloads the support files automatically.

Results, downloaded data, and completed model checkpoints are saved in
`MyDrive/CS183/HW3-2026/`. Save the edited notebook separately in Colab.
The LSTM checkpoint is saved after training; translation checkpoints are saved
when validation accuracy improves. An interrupted training epoch does not resume
automatically. Rerunning a training cell trains the model again.

## Submit to Gradescope

Follow the notebook's submission instructions:

- Export the completed notebook, including answers to the starred questions,
  as **HW3.pdf**.
- Submit the generated **`.json` and `.npy` files inside `results/`** with their
  original filenames. Upload the result files directly so the autograder can
  find them at the submission root.
- Include both baseline and attention beam-search prediction files if completing
  the extra-credit section.

Model checkpoints and downloaded datasets are not submission files.

## Run locally

Use Python 3.12 and an NVIDIA GPU. From the repository directory:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-local.txt
jupyter lab hw3.ipynb
```

Select this environment's notebook kernel. Local runs write results and
checkpoints into the repository directory and skip Google Drive mounting.
After installing or changing packages in a running kernel, restart it before
running the notebook.

All data loading, batching, training, and evaluation code is in the notebook.
The only Python support file is `colab_setup.py`, which installs pinned
dependencies while keeping Colab's supplied PyTorch and CUDA.
