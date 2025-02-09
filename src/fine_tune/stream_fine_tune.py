from time import sleep
import requests
import os, argparse
import openai, yaml
import mlflow, time
import pandas as pd
from fine_tune import load_api_key, wait_for_job_completion, load_yaml


def main():
  parser = argparse.ArgumentParser()
  # add optional argument fine_tune_id
  parser.add_argument("--fine_tune_id", type=str, default=None)
  parser.add_argument("--fine_tune_metadata", default="./data/4fine_tune")
  parser.add_argument("--aoai_resource_name", default="aoai")
  parser.add_argument("--api_version", default="2022-06-01-preview")
  args = parser.parse_args()

  api_key = load_api_key()
  if not args.fine_tune_id:
    args.fine_tune_id = load_yaml(f"{args.fine_tune_metadata}/MLArtifact.yaml")["id"]

  url = f"https://{args.aoai_resource_name}.openai.azure.com"

  data = wait_for_job_completion(url + "/openai/fine-tunes", api_key, args.fine_tune_id, args)
  print(data)

if __name__ == "__main__":
  main()
