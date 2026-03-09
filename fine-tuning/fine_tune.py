"""Submit and monitor an OpenAI fine-tuning job."""

import os
import sys
import time
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TRAINING_FILE = Path(__file__).parent / "training_data.jsonl"
BASE_MODEL = "gpt-4o-mini-2024-07-18"


def validate_training_data():
    """Basic validation of the training JSONL file."""
    import json

    if not TRAINING_FILE.exists():
        print(f"ERROR: {TRAINING_FILE} not found. Run generate_training.py first.")
        sys.exit(1)

    with open(TRAINING_FILE) as f:
        lines = f.readlines()

    if len(lines) < 10:
        print(f"WARNING: Only {len(lines)} examples. OpenAI recommends at least 10, ideally 50-100.")

    errors = 0
    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
            messages = data.get("messages", [])
            if len(messages) != 3:
                print(f"  Line {i+1}: Expected 3 messages (system/user/assistant), got {len(messages)}")
                errors += 1
            roles = [m["role"] for m in messages]
            if roles != ["system", "user", "assistant"]:
                print(f"  Line {i+1}: Unexpected roles: {roles}")
                errors += 1
        except json.JSONDecodeError:
            print(f"  Line {i+1}: Invalid JSON")
            errors += 1

    print(f"Validation: {len(lines)} examples, {errors} errors")
    if errors > 0:
        print("Fix errors before proceeding.")
        sys.exit(1)
    return len(lines)


def upload_and_finetune():
    """Upload training file and create fine-tuning job."""
    print(f"Uploading {TRAINING_FILE}...")
    with open(TRAINING_FILE, "rb") as f:
        file_obj = client.files.create(file=f, purpose="fine-tune")
    print(f"Uploaded: {file_obj.id}")

    print(f"\nCreating fine-tuning job on {BASE_MODEL}...")
    job = client.fine_tuning.jobs.create(
        training_file=file_obj.id,
        model=BASE_MODEL,
        suffix="badnews-primalrace",
        hyperparameters={
            "n_epochs": 3,
        },
    )
    print(f"Job created: {job.id}")
    print(f"Status: {job.status}")

    print("\nMonitoring job progress...")
    while True:
        job = client.fine_tuning.jobs.retrieve(job.id)
        print(f"  Status: {job.status}", end="")
        if job.status == "succeeded":
            print(f"\n\nFine-tuning complete!")
            print(f"Fine-tuned model: {job.fine_tuned_model}")
            print(f"\nUpdate your .env file:")
            print(f'  FINE_TUNED_MODEL="{job.fine_tuned_model}"')
            return job.fine_tuned_model
        elif job.status == "failed":
            print(f"\n\nFine-tuning FAILED: {job.error}")
            sys.exit(1)
        elif job.status == "cancelled":
            print(f"\n\nFine-tuning was cancelled.")
            sys.exit(1)
        else:
            print(" (waiting 30s...)")
            time.sleep(30)


def main():
    print("=== Bad News Platform: Fine-Tuning Pipeline ===\n")
    num_examples = validate_training_data()
    print(f"\nReady to fine-tune with {num_examples} examples on {BASE_MODEL}")

    confirm = "y"

    model_name = upload_and_finetune()
    print(f"\nDone. Model: {model_name}")


if __name__ == "__main__":
    main()
