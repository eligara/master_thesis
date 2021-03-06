from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


def get_generic_tissue_from_specific(tissue, samples=None):
    if tissue in samples['secondary_site']:
        return samples[samples['secondary_site']==tissue]['primary_site'].values[0]
    else:
        return tissue

def get_specific_mapping_to(tissue, samples=None):
    if tissue in samples['primary_site']:
        return samples[samples['primary_site']==tissue]['secondary_site'].unique()
    else:
        return tissue

def get_gtex_tissue(sample, samples=None):
    for fullsample in samples.index.values:
        if sample in fullsample:
            return samples.loc[fullsample,:]

def makePie(df_clusters, level, c, whatToLookFor = ['primary_site','secondary_site'], samples=None):
    c=int(c)
    level=int(level)
    fig = plt.figure(figsize=(60,15))
    ax = fig.subplots(1, len(whatToLookFor))
    for i,lookFor in enumerate(whatToLookFor):
        datatotestarr = []
        for sample in df_clusters['Cluster %d'%c].dropna():
            try:
                datatotestarr.append(get_gtex_tissue(sample)[lookFor])
            except:
                print("error with %s"%sample)
        utype, counts = np.unique(datatotestarr, return_counts=True)
        total = len(datatotestarr)
        try:
            labels = ['\n'.join(wrap(str(l), 20)) for l in utype]
        except:
            labels = utype
        ax[i].set_title(lookFor, fontsize=44)
        patches, texts, autotexts = ax[i].pie(counts,
                                              labels=labels,
                                              autopct=lambda p: '#:%.0f'%(p * total / 100),
                                              textprops={'fontsize':30, 'color':'white', 'wrap':True})
        for t in texts:
            t.set_fontsize(24)
            t.set_wrap(True)
            t.set_color('black')
    fig.savefig("cluster_pie_level_%d_cluster_%d.png"%(level, c))
