### ML vs LLM
As ML engineers who want to interact with LLMs, and foundation models in general, is that we can no longer assume we have access to
the `model artifact`, the `training data`, or `testing data`. 
We have to instead treat the model as a third-party service that we should call out to for consumption. Luckily, there are many tools and techniques for implementing this.

LangChain  provides a wide variety of functionality that is useful when dealing with NLP and text-based applications
more generally. 
For example, there are utilities for text splitting, working
with vector databases, document loading and retrieval, and conversational state persistence, among others. 


### Project goal

1. I want to be given clear `labels of anomalous rides` that have anomalously `long ride times `or `distances`
so that I can perform further analysis and modeling on the volume of anomalous rides.
2. I want to be provided with a `summary of relevant textual data` 
so that I can do further analysis and modeling on the reasons for some rides being anomalous.
3. I want all `output data sent to a central location, preferably in the cloud`, 
so that I can easily build dashboards.
4. I would like to see the output data for the `previous day’s rides every morning` 
so that I can  provide an update to the logistics managers

The requirements for our problem have stipulated that we have `relatively small datasets` 
that need to be `processed in batches` every day, first with some kind of clustering or anomaly detection
algorithm before further analysis using an LLM. 

Data storage and interface options: `AWS S3`
Modeling part with small data set: `Scikit-learn`
Text summarization component: `GPT-X models from OpenAI`
Manage our scheduling: `Airflow`


### Technical Specification
we will actually perform the ETML process twice: once for the clustering component and
once for the text summarization. 

Doing it this way means that we can use intermediary storage in between the steps, in this case, AWS S3 again, in
order to introduce some resiliency into the system. This is so because if the second step fails, it doesn’t mean the first step’s processing is lost. 


### How advanced Airflow features helps in ELML process
Good DAG design practices:
#### 1. Embody separation of concerns for your tasks:
At the level of Airflow DAGs we can embody this principle by ensuring our DAGs are built of tasks that have one clear job to do in each case. So, in this example we clearly have the “extract,” “transform,” “ML,” and “load” stages, for which it makes sense to have specific tasks in each case. 
##### Advantage: 
This also helps us to create good control flows and error handling.

#### 2. Use retries:
An important aspect of this is the concept of “retries,” which tells the task to, you guessed it, try the process again if there is a failure. You can also introduce delays between retries and even exponential backoff, which is when your retries have increasing time delays between them. 

#### 3. Mandate idempotency in your DAGs:
Idempotency is the quality of code that returns the same result when run multiple times on the same inputs. 
The challenge for an EMTL application is that we obviously have ML models, for example,
ML models in scikit-learn or neural networks in PyTorch.


#### Configuring Airflow using Docker-Compose 
![alt text](image.png)


