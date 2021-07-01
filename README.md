# BinaryCoP
Binary Neural Network-based COVID-19 Face-Mask Wear and Positioning Predictor on Edge Devices

### XOHW Team Number: xohw21-142

High Performance (Multi-Gate/Camera)             |  Low Power (Single Gate/Camera)
:-------------------------:|:-------------------------:
![](docs/imgs/firsthalf.gif?raw=true "Overview")  |  ![](docs/imgs/secondhalf.gif?raw=true "Overview")


## Our Goal
Deploy **accurate, unbiased** image classification algorithms, which can be used at entrances or speed-gates to check **correct mask wear and positioning**, with all processing on **low-power, cheap, edge** hardware to **preserve privacy** of passing users.
![Alt text](docs/imgs/bincop.png?raw=true "Overview")

## Example Notebook and Documentation
* Example Jupyter notebook to test a prototype of BinaryCoP on a standard PYNQ-board. 
* Docs contains extended report and slides.
* Other Utils: 
    - Script to generate Grad-CAM interpretability results from trained networks.
    - DSP-BitPacking script to rewire XNOR operations through DSP blocks.

## Requirements and Dependencies
* PYNQ-Z1 with PYNQ 2.5 image.
* DSP-BitPacking synthesis tested on Vivado 2018.1 with BNN-PYNQ.

## Citation

This repository is based on the work published in IPDPS-RAW 2021.

    @inproceedings{bcop,
    author={Fasfous, Nael and Vemparala, Manoj-Rohit and Frickenstein, Alexander and Frickenstein, Lukas and Badawy, Mohamed and Stechele, Walter},
    booktitle={2021 IEEE International Parallel and Distributed Processing Symposium Workshops (IPDPSW)},
    title={BinaryCoP: Binary Neural Network-based COVID-19 Face-Mask Wear and Positioning Predictor on Edge Devices},
    year={2021},
    pages={108-115},
    doi={10.1109/IPDPSW52791.2021.00024}}

Acknowledgements:

    @inproceedings{finn,
    author = {Umuroglu, Yaman and Fraser, Nicholas J. and Gambardella, Giulio and Blott, Michaela and Leong, Philip and Jahre, Magnus and Vissers, Kees},
    title = {FINN: A Framework for Fast, Scalable Binarized Neural Network Inference},
    booktitle = {Proceedings of the 2017 ACM/SIGDA International Symposium on Field-Programmable Gate Arrays},
    series = {FPGA '17},
    year = {2017},
    pages = {65--74},
    publisher = {ACM}}

    @article{cabani.hammoudi.2020.maskedfacenet,
    title={MaskedFace-Net -- A Dataset of Correctly/Incorrectly Masked Face Images in the Context of COVID-19},
    author={Adnane Cabani and Karim Hammoudi and Halim Benhabiles and Mahmoud Melkemi},
    journal={Smart Health},
    year={2020},
    url ={http://www.sciencedirect.com/science/article/pii/S2352648320300362},
    issn={2352-6483},
    doi ={https://doi.org/10.1016/j.smhl.2020.100144}}
