# Interpretability and Synthetic Data

<img src="/docs/imgs/gcam.png" width="600">

Google Drive link to Grad-CAM results [LINK](https://drive.google.com/drive/folders/1AmgOKRiI6klRwWUbMiDlNMz52k9Ls827?usp=sharing)

We use interpretability tools to assert that sensible features are being learned. 
This is particularly important when using synthetic data to train a neural network. 
Synthetic data generation can lead to artifacts which a neural network may "latch" onto to make its predictions, leading to good training performance, but poor performance when deployed.

**Note:** All CAMs presented are based on accurate preditions with respect to ground truth.

## Main Observations:
* BinaryCoP focuses on key facial lineaments of the human wearing the mask, rather than the mask itself. This potentially helps in generalizing on other mask types.
* The Region of Interest (RoI) curves finely above the mask, tracing the exposed region of the face. For Chin exposed examples, the RoI is heated near the chin area.
* For the Nose-and-Mouth exposed class, models seem to distribute their attention onto several exposed features of the face.
* BinaryCoP generalizes over ages, hair colors and head gear, as well as complete face manipulation with double-masks, face paint and sunglasses.
* In some cases, FP32 makes predictions based on unrelated features (random heat-maps on irrelevant parts of image). This may indicate FP32 overtfitting easily on the dataset, compared to BNNs.

## Generate Grad-CAMs
1) Extract gradients from training toolbox (e.g. Pytorch/Brevitas, Theano/BNN) as numpy (.npz) files.
2) Gradients should be dy_prediction/dx_Activation, where x_Activation are the activations of the Conv. layer to be interpreted by Grad-CAM.
3) Provide the Raw input image to the script.
4) Execute Script (outputs: RawImage, HeatMap, Overlaid G-CAM) - Requires TF1.


## CAM for Classes
For full discussion, please refer to the BinaryCoP paper.

<img src="/docs/imgs/gcam_classes.png" width="600">

## CAM for Generalizability
For full discussion, please refer to the BinaryCoP paper.

<img src="/docs/imgs/gcam_generalization.png" width="600">
