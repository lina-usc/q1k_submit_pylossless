import re
import subprocess

# Function to extract details from filename
def extract_job_info(filename):
    # Define the pattern to capture the required sections
    pattern = r"sub-(.*?)_ses-(.*?)_task-(.*?)_run-(.*?)_eeg\.edf"
    match = re.match(pattern, filename)

    if match:
        # Extract the groups from the match
        subject_id = match.group(1)
        session_id = match.group(2)
        task_id = match.group(3)
        run_id = match.group(4)
        return subject_id, session_id, task_id, run_id
    else:
        raise ValueError("Filename pattern did not match.")

# Function to submit job to Slurm scheduler
def submit_slurm_job(project_path, filename):
    
    out_file = filename.replace(".edf", ".out")
    job_name = filename.replace(".edf", "_pyll")

    # Extract job info from filename
    subject_id, session_id, task_id, run_id = extract_job_info(filename)
    
    # Construct the sbatch command
    sbatch_command = [
        'sbatch',
        '--job-name=' + job_name,
        '--output=slurm_output/' +  out_file,
        'q1k_pyll_jobsub.sh',
        project_path,
        subject_id,
        session_id,
        task_id,
        run_id,
        project_path,
    ]

    # Print the command to check it before submission
    print("Running command:", ' '.join(sbatch_command))

    # Submit the job using subprocess
    try:
        result = subprocess.run(sbatch_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Job submitted successfully!")
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Error submitting job:", e.stderr.decode())

    return sbatch_command, result
