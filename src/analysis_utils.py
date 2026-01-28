"""Small plotting and helpers for analysis notebooks."""
import matplotlib.pyplot as plt
import seaborn as sns

def save_hist(series, outpath, title=None):
    plt.figure(figsize=(6,4))
    sns.histplot(series.dropna(), bins=80)
    if title:
        plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()
