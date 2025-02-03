//Aim: To perform Report Superstep on Hillman Ltd using Python
from time import time 
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import offsetbox 
from sklearn import ( 
    manifold, datasets, decomposition, ensemble, 
    discriminant_analysis, random_projection 
) 
# Load the dataset 
digits = datasets.load_digits(n_class=6) 
X = digits.data 
y = digits.target 
n_samples, n_features = X.shape 
n_neighbors = 30 
 
def plot_embedding(X, title=None): 
    x_min, x_max = np.min(X, 0), np.max(X, 0) 
    X = (X - x_min) / (x_max - x_min) 
    plt.figure(figsize=(10, 10)) 
    ax = plt.subplot(111) 
     
    for i in range(X.shape[0]): 
        plt.text( 
            X[i, 0], X[i, 1], str(digits.target[i]), 
            color=plt.cm.Set1(y[i] / 10.), fontdict={'weight': 'bold', 'size': 9}) 
    if hasattr(offsetbox, 'AnnotationBbox'): 
        # Only print thumbnails with matplotlib > 1.0 
        shown_images = np.array([[1., 1.]])   
        for i in range(digits.data.shape[0]): 
            dist = np.sum((X[i] - shown_images) ** 2, axis=1) 
            if np.min(dist) < 4e-3: 
                continue  
            shown_images = np.r_[shown_images, [X[i]]] 
            imagebox = offsetbox.AnnotationBbox( 
                offsetbox.OffsetImage(digits.images[i], 
cmap=plt.cm.gray_r), 
                X[i]) 
            ax.add_artist(imagebox) 
    plt.xticks([]), plt.yticks([]) 
    if title is not None: 
        plt.title(title) 
 
# Plotting a selection of the dataset 
n_img_per_row = 20 
img = np.zeros((10 * n_img_per_row, 10 * n_img_per_row)) 
for i in range(n_img_per_row): 
    ix = 10 * i + 1 
    for j in range(n_img_per_row): 
        iy = 10 * j + 1 
        img[ix:ix + 8, iy:iy + 8] = X[i * n_img_per_row + 
j].reshape((8, 8)) 
plt.figure(figsize=(10, 10)) 
plt.imshow(img, cmap=plt.cm.binary) 
plt.xticks([]), plt.yticks([])
plt.title('A selection from the 64-dimensional digits dataset') 
 
# Projections and embeddings 
# Random Projection 
print("1.)Computing random projection") 
rp = random_projection.SparseRandomProjection(n_components=2, 
random_state=42) 
X_projected = rp.fit_transform(X) 
plot_embedding(X_projected, "Random Projection of the digits") 
 
# PCA Projection 
print("2.)Computing PCA projection") 
t0 = time() 
X_pca = 
decomposition.TruncatedSVD(n_components=2).fit_transform(X) 
plot_embedding(X_pca, f"Principal Components projection of the 
digits (time {time() - t0:.2f}s)") 
 
# Linear Discriminant Analysis Projection 
print("3.)Computing Linear Discriminant Analysis projection") 
X2 = X.copy() 
X2.flat[::X.shape[1] + 1] += 0.01  # Make X invertible 
t0 = time() 
X_lda = 
discriminant_analysis.LinearDiscriminantAnalysis(n_components=2)
 .fit_transform(X2, y) 
plot_embedding(X_lda, f"Linear Discriminant projection of the 
digits (time {time() - t0:.2f}s)") 
 
# Isomap Embedding 
print("4.)Computing Isomap embedding") 
t0 = time() 
X_iso = manifold.Isomap(n_neighbors=n_neighbors, 
n_components=2).fit_transform(X) 
plot_embedding(X_iso, f"Isomap projection of the digits (time 
{time() - t0:.2f}s)") 
 
# Locally Linear Embedding 
print("5.)Computing Locally Linear Embedding") 
clf = manifold.LocallyLinearEmbedding(n_neighbors=n_neighbors, 
n_components=2, method='standard') 
t0 = time() 
X_lle = clf.fit_transform(X) 
plot_embedding(X_lle, f"Locally Linear Embedding of the digits 
(time {time() - t0:.2f}s)") 
 
# Modified LLE Embedding 
print("6.)Computing modified LLE embedding") 
clf = manifold.LocallyLinearEmbedding(n_neighbors=n_neighbors, 
n_components=2, method='modified') 
t0 = time() 
X_mlle = clf.fit_transform(X) 
plot_embedding(X_mlle, f"Modified Locally Linear Embedding of 
the digits (time {time() - t0:.2f}s)") 
 
# Hessian LLE Embedding 
print("7.)Computing Hessian LLE embedding") 
clf = manifold.LocallyLinearEmbedding(n_neighbors=n_neighbors, 
n_components=2, method='hessian') 
t0 = time() 
X_hlle = clf.fit_transform(X) 
plot_embedding(X_hlle, f"Hessian Locally Linear Embedding of the 
digits (time {time() - t0:.2f}s)")

# LTSA Embedding 
print("8.)Computing LTSA embedding") 
clf = manifold.LocallyLinearEmbedding(n_neighbors=n_neighbors, 
n_components=2, method='ltsa') 
t0 = time() 
X_ltsa = clf.fit_transform(X) 
plot_embedding(X_ltsa, f"Local Tangent Space Alignment of the 
digits (time {time() - t0:.2f}s)") 
# MDS Embedding 
print("9.)Computing MDS embedding") 
clf = manifold.MDS(n_components=2, n_init=1, max_iter=100) 
t0 = time() 
X_mds = clf.fit_transform(X) 
plot_embedding(X_mds, f"MDS embedding of the digits (time 
{time() - t0:.2f}s)") 
 
# Random Trees Embedding 
print("10.)Computing Totally Random Trees embedding") 
hasher = ensemble.RandomTreesEmbedding(n_estimators=200, 
random_state=0, max_depth=5) 
t0 = time() 
X_transformed = hasher.fit_transform(X) 
pca = decomposition.TruncatedSVD(n_components=2) 
X_reduced = pca.fit_transform(X_transformed) 
plot_embedding(X_reduced, f"Random forest embedding of the 
digits (time {time() - t0:.2f}s)") 
 
# Spectral Embedding 
print("11.)Computing Spectral embedding") 
embedder = manifold.SpectralEmbedding(n_components=2, 
random_state=0, eigen_solver="arpack")
t0 = time() 
X_se = embedder.fit_transform(X) 
plot_embedding(X_se, f"Spectral embedding of the digits (time 
{time() - t0:.2f}s)") 
 
# t-SNE Embedding 
print("12.)Computing t-SNE embedding") 
tsne = manifold.TSNE(n_components=2, init='pca', random_state=0) 
t0 = time() 
X_tsne = tsne.fit_transform(X) 
plot_embedding(X_tsne, f"t-SNE embedding of the digits (time 
{time() - t0:.2f}s)") 
plt.show() 
print("Execution Done.")
