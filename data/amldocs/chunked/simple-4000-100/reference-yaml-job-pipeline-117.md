
## YAML: common pipeline job settings

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json
type: pipeline
display_name: hello_pipeline_settings

settings:
  default_datastore: azureml:workspaceblobstore
  default_compute: azureml:cpu-cluster
jobs:
  hello_job:
    command: echo 202204190 & echo "hello"
    environment: azureml:AzureML-sklearn-1.0-ubuntu20.04-py38-cpu:1
  world_job:
    command: echo 202204190 & echo "hello"
    environment: azureml:AzureML-sklearn-1.0-ubuntu20.04-py38-cpu:1   
```

## YAML: top-level input and overriding common pipeline job settings

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json
type: pipeline
display_name: hello_pipeline_abc
settings:
    default_compute: azureml:cpu-cluster
  
inputs:
  hello_string_top_level_input: "hello world"
jobs:
  a:
    command: echo hello ${{inputs.hello_string}}
    environment: azureml:AzureML-sklearn-1.0-ubuntu20.04-py38-cpu@latest
    inputs:
      hello_string: ${{parent.inputs.hello_string_top_level_input}}
  b:
    command: echo "world" >> ${{outputs.world_output}}/world.txt
    environment: azureml:AzureML-sklearn-1.0-ubuntu20.04-py38-cpu@latest
    outputs:
      world_output:
  c:
    command: echo ${{inputs.world_input}}/world.txt
    environment: azureml:AzureML-sklearn-1.0-ubuntu20.04-py38-cpu@latest
    inputs:
      world_input: ${{parent.jobs.b.outputs.world_output}}
 
```

<!-- ## YAML: model training pipeline

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json
type: pipeline

description: Pipeline using distributed job to train model based on cifar-10 dataset

display_name: cifar-10-pipeline-example
experiment_name: cifar-10-pipeline-example
jobs:
  get_data:
    type: command
    command: >-
      wget https://azuremlexamples.blob.core.windows.net/datasets/cifar-10-python.tar.gz;
      tar -xvzf cifar-10-python.tar.gz -C ${{outputs.cifar}};
      rm cifar-10-python.tar.gz;
    compute: azureml:gpu-cluster
    environment: azureml:AzureML-sklearn-1.0-ubuntu20.04-py38-cpu@latest
    outputs:
      cifar:
        type: uri_folder
        mode: upload
  train_model:
    type: command
    command: >-
      python main.py
      --data-dir ${{inputs.cifar}}
      --epochs ${{inputs.epochs}}
      --model-dir ${{outputs.model_dir}}
    code: src/train-model
    inputs:
      epochs: 1
      cifar: ${{parent.jobs.get_data.outputs.cifar}}
    outputs:
      model_dir:
        type: uri_folder
        mode: upload
    environment: azureml:AzureML-pytorch-1.9-ubuntu18.04-py37-cuda11-gpu:26
    compute: azureml:gpu-cluster
    distribution:
      type: pytorch
      process_count_per_instance: 1
    resources:
      instance_count: 2
  eval_model:
    type: command
    command: >-
      python main.py
      --data-dir ${{inputs.cifar}}
      --model-dir ${{inputs.model_dir}}/model
    code: src/eval-model
    environment: azureml:AzureML-pytorch-1.9-ubuntu18.04-py37-cuda11-gpu:26
    compute: azureml:gpu-cluster
    distribution:
      type: pytorch
      process_count_per_instance: 1
    resources:
      instance_count: 2
    inputs:
      cifar: ${{parent.jobs.get_data.outputs.cifar}}
      model_dir: ${{parent.jobs.train_model.outputs.model_dir}}

```

## Next steps

- [Install and use the CLI (v2)](how-to-configure-cli.md)
- [Create ML pipelines using components](how-to-create-component-pipelines-cli.md)
