Segmentation de lésions dermoscopiques — Méthode **LBP Clustering (LC)**

**Objectif** : Segmenter automatiquement une lésion dermoscopique (masque binaire) à partir d’une image **RGB** via un pipeline non supervisé fondé sur la méthode **Local Binary Patterns (LBP)** + **k-means++** après une transformation d’espace judicieusement choisie. Méthode décrite et évaluée dans **Pereira et al., 2020** (Dermoscopic skin lesion image segmentation based on Local Binary Pattern Clustering).

> **Hypothèses / Pré‑requis.** Image dermoscopique couleur **RGB uint8**. Le pré‑traitement (retrait des poils, correction vignettage…) peut être traité séparément. Si nécessaire : suppression du **cadre noir** par la Lightness HSL et **filtre médian** de taille proportionnelle à l’image avant segmentation.

---

## Pipeline (étapes à implémenter)

1. **Luminance (Y)**  
   Convertir l’image **RGB** en luminance **Y** avec la pondération **BT.601** : \(Y = 0.299R + 0.587G + 0.114B\). Cette luminance sert d’entrée aux LBP.

2. **LBP \(P=8, R=1\)**  
   Calculer, pour chaque pixel, le **LBP** sur un voisinage 3×3 :
   \( \mathrm{LBP}(x)=\sum_{p=0}^{7} s(I_p-I_c)\,2^p,\; s(u)=\mathbf{1}[u>0] \).
   On obtient des codes dans \([0,255]\). 

3. **Binarisation par sous‑ensemble de motifs**  
   Conserver uniquement les motifs **LBP = 0** et **puissances de 2** (i.e. \(\{0,2^n\}\)), posés à **0** ; tous les autres codes deviennent **1**. Les **1** se concentrent dans la **lésion** (textures non lisses).

4. **Lissage gaussien → image L**  
   Appliquer un filtre **Gaussien 2D** (\(\sigma=3\), **noyau 13×13**) à l’image binaire précédente pour produire **L** \(\in [0,1]\), qui homogénéise la région lésion.

5. **Empilement & changement d’espace**  
   Former un pseudo‑RGB **S = [L, Y, L]**, puis convertir **S → CIE L\*a\*b\*** et **conserver (a\*, b\*)**. Cette transformation **sépare mieux** peau (vert, \(a^*<0\)) et lésion (rose/rouge), facilitant le clustering.

6. **Clustering k‑means++ (K=2)**  
   Appliquer **k‑means++** (distance euclidienne) sur les paires de caractéristiques **(a\*, b\*)** (répéter 3 fois, **max 100 itérations**, garder la meilleure solution SSE).

7. **Sélection automatique du cluster “lésion”**  
   Entre les deux segments, choisir celui dont la moyenne de **\(\max(a^*,0) - \min(b^*,0)\)** est **maximale** (critère de *pinkness*). Le vert de la peau tire \(a^*\) vers le négatif.

8. **Post‑traitement léger**  
   Effectuer une **ouverture morphologique** (structurant disque), **remplir les trous** et **ne garder qu’une composante** (p.ex. la plus grande). Des opérations morphologiques analogues sont employées classiquement en segmentation dermoscopique.

---

## Paramètres par défaut (recommandés)

- **LBP** : \(P=8\), \(R=1\).
- **Gaussien** : \(\sigma=3\), **taille 13×13**.
- **k‑means++** : **K=2**, **n\_init = 3**, **max\_iter = 100**.

---

## Sorties

- **Masque binaire** \(H\times W\) (1 = lésion, 0 = peau).
- (Option) **Overlay** : contour du masque superposé à l’image RGB pour la visualisation.

---

## Remarques

- La méthode **fonctionne aussi** si la lésion n’est pas ronde ou présente des **bords flous**, grâce au rôle de LBP + lissage avant clustering.
- En amont, si besoin : **cadre noir** par Lightness HSL < 20 % et **filtre médian** proportionnel à la taille d’image (réduit bulles/poils).

---

## Références 

- **Pereira et al., 2020.** Dermoscopic skin lesion segmentation based on Local Binary Pattern Clustering: *pipeline LBP→subset→Gauss→[L,Y,L]→Lab(a*,b*)→k-means++→pinkness*.
- **Célébi et al., 2008.** SRM en dermoscopie : détaille des **pré‑/post‑traitements** standards (cadre noir, médian, morphologie) utiles à intégrer dans la chaîne complète.
