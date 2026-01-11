
from datasets import load_dataset
from swebench.collect.print_pulls import main as print_pulls
from swebench.harness.run_evaluation import main as run_evaluation


def get_raw_swe_bench_hf(dataset_name: str = "princeton-nlp/SWE-bench", split: str = "train"):
    """
    Load raw SWE-bench dataset from HuggingFace.
    
    https://huggingface.co/datasets/SWE-bench/SWE-bench
    
    Args:
        dataset_name (str): Name of the dataset. Options:
            - "princeton-nlp/SWE-bench" (default) - Full dataset with train/test/dev splits
            - "SWE-bench/SWE-bench_Lite" - Lite version
            - "SWE-bench/SWE-bench_Verified" - Verified dataset (test split only)
            - "SWE-bench/SWE-bench_Multimodal" - Multimodal dataset
        split (str): Dataset split to load. Options: "train", "test", "dev". Default: "train"
            Note: Not all datasets have all splits (e.g., Verified only has "test")
    
    Returns:
        datasets.Dataset: The loaded SWE-bench dataset
    """
    dataset = load_dataset(dataset_name, split=split)
    return dataset


def collect_github_prs(
    repo_name: str,
    output: str,
    token: str = None,
    max_pulls: int = None,
    cutoff_date: str = None,
    pull_number: int = None,
):
    print_pulls(
        repo_name=repo_name,
        output=output,
        token=token,
        max_pulls=max_pulls,
        cutoff_date=cutoff_date,
        pull_number=pull_number,
    )


def evaluate_submission(
    dataset_name: str,
    split: str,
    predictions_path: str,
    run_id: str,
    instance_ids: list = None,
    max_workers: int = 4,
    timeout: int = 1800,
    force_rebuild: bool = False,
    cache_level: str = "none",
    clean: bool = False,
    open_file_limit: int = 4096,
    namespace: str = None,
    rewrite_reports: bool = False,
    modal: bool = False,
    instance_image_tag: str = "latest",
    env_image_tag: str = "latest",
    report_dir: str = ".",
):
    return run_evaluation(
        dataset_name=dataset_name,
        split=split,
        instance_ids=instance_ids,
        predictions_path=predictions_path,
        max_workers=max_workers,
        force_rebuild=force_rebuild,
        cache_level=cache_level,
        clean=clean,
        open_file_limit=open_file_limit,
        run_id=run_id,
        timeout=timeout,
        namespace=namespace,
        rewrite_reports=rewrite_reports,
        modal=modal,
        instance_image_tag=instance_image_tag,
        env_image_tag=env_image_tag,
        report_dir=report_dir,
    )

def main():
    dataset = get_raw_swe_bench_hf()
    print(dataset)


if __name__ == "__main__":
    main()