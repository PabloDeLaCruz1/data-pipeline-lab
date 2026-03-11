from prefect import flow, task
import subprocess


@task
def run_ingestion():
    subprocess.run(["python", "ingestion/load_sample.py"], check=True)


@flow(name="data-pipeline-lab")
def pipeline_flow():
    run_ingestion()


if __name__ == "__main__":
    pipeline_flow()
