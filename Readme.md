## Project Structure 
ZenML is a completely open-source framework that helps you write ML
pipelines in a way that is totally abstracted from the underlying infrastructure. This means that your local development environment and your eventual production environment can be very different, and can be
changed through changes in configuration without altering the core of
your pipelines. 


### Setup ZenML
ZenML also comes with a series of existing templates you can leverage,
which you can install with:
`poetry add "zenml[templates]"`

#### Install Starter Template project with a MLOPs template
`poetry run zenml init --template starter`

#### Install ZenML server
`poetry add "zenml[server]" `


#### Run the pipeline
##### Run the feature engineering pipeline
   ` python run.py --feature-pipeline`
  
  
##### Run the training pipeline
    `python run.py --training-pipeline `

We'll start with two simple models, a SGD Classifier and a Random Forest
Classifier, both batteries-included from `sklearn`. We'll train them both on the
same data and then compare their performance.

##### Run the training pipeline with versioned artifacts
    `python run.py --training-pipeline --train-dataset-version-name=1 --test-dataset-version-name=1`

Luckily, ZenML offers a *Model Control Plane*, which is a central register of all your ML models.    

##### Run the inference pipeline
    `python run.py --inference-pipeline `

