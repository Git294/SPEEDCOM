<p align="center"><img src="doc/source/logos/simpleLogo.png" alt="SPEEDCOM" title="SPEEDCOM"/></p>

_**S**pectra **P**rediction for the **E**xcitation and **E**mission of **D**yes and other **C**onjugated **O**rganic **M**olecules_

#### Authors: **J. Abbott**, **R. Beck**, **H. Hu**, **Y. Liu**, **L. Lu**.

SPEEDCOM is a python package that aims to predict the fluorescence emission and absorption spectra of small conjugated organic molecules. Prediction algorithms are implemented with [tensorflow](https://github.com/tensorflow/tensorflow) and [keras](https://github.com/keras-team/keras), trained on data from the [PhotochemCAD database](http://www.photochemcad.com/PhotochemCAD.html). The software has a graphical-user-interface (GUI) where users can input the [SMILES](https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system) string for a given molecule to be returned its predicted spectra. 