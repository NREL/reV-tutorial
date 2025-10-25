Let me help you understand what's happening with your SLURM job submissions and node allocation in AWS ParallelCluster.

    Retrieving knowledge

    Retrieving knowledge

Based on the AWS ParallelCluster documentation, I can explain what's happening when you submit multiple jobs requesting 1 node each but only see one node checked out. This is due to SLURM's default node sharing behavior in AWS ParallelCluster.
Why Multiple Jobs Share One Node
Default SLURM Behavior:

By default, SLURM allows multiple jobs to share the same node unless you explicitly request exclusive access. When you submit jobs with -N 1
(requesting 1 node), SLURM will:

    Pack multiple jobs onto the same node if there are available resources (CPU cores, memory)
    Only launch additional nodes when the current node(s) are fully utilized
    Share node resources among jobs based on their specific resource requests

What You're Seeing:

# Multiple jobs submitted like this:
sbatch -N 1 --wrap "my_job_1"
sbatch -N 1 --wrap "my_job_2" 
sbatch -N 1 --wrap "my_job_3"

Result: All jobs may run on the same single EC2 instance (node) if there are sufficient resources.
How to Get Exclusive Node Access
Option 1: Use the --exclusive
Flag

sbatch -N 1 --exclusive --wrap "my_job"

This ensures each job gets exclusive access to its allocated node(s).
Option 2: Request Specific Resources

# Request all CPUs on the node
sbatch -N 1 --cpus-per-task=4 --wrap "my_job"  # for a 4-vCPU instance

# Request all memory on the node  
sbatch -N 1 --mem=7500M --wrap "my_job"  # for an 8GB instance

Option 3: Configure Queue for Exclusive Allocation

Set JobExclusiveAllocation = true
in your cluster configuration for specific queues.
Understanding Node States in sinfo

When you run sinfo
, you'll see different node states:

$ sinfo
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
queue1*      up   infinite      1    mix queue1-dy-c5xlarge-1
queue1*      up   infinite      4  idle~ queue1-dy-c5xlarge-[2-5]

Node States:

    idle
    : Node is available but not running jobs
    mix
    : Node is partially allocated (some jobs running, some resources available)
    alloc
    : Node is fully allocated to jobs
    idle~
    : Dynamic node in power-saving mode (not launched yet)

Memory-Based Scheduling Impact

The documentation specifically mentions this behavior:

    "When memory-based scheduling is enabled, if no memory option is included (--mem
    , --mem-per-cpu
    , or --mem-per-gpu
    ), Slurm assigns entire memory of the allocated nodes to the job, even if it requests only a portion of the other resources, such as CPUs or GPUs. This effectively prevents node sharing until the job is finished because no memory is available to other jobs."

Solution for Memory-Based Scheduling:

# Specify memory requirements to allow sharing
sbatch -N 1 --mem=2000M --wrap "my_job"  # Request specific memory amount

Checking Job Allocation

Use these commands to see how jobs are distributed:

# See job allocation
$ squeue
JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
   1      queue1     wrap ec2-user  R       0:30      1 queue1-dy-c5xlarge-1
   2      queue1     wrap ec2-user  R       0:25      1 queue1-dy-c5xlarge-1
   3      queue1     wrap ec2-user  R       0:20      1 queue1-dy-c5xlarge-1

# See detailed node information
$ scontrol show nodes queue1-dy-c5xlarge-1

Best Practices
For Exclusive Node Access:

sbatch -N 1 --exclusive --wrap "my_parallel_job"

For Resource-Specific Jobs:

# Request specific resources to control sharing
sbatch -N 1 --cpus-per-task=2 --mem=4000M --wrap "my_job"

For MPI Jobs:

# Typically want exclusive access for MPI
sbatch -N 2 --exclusive --wrap "mpirun -np 8 my_mpi_program"

Summary

The behavior you're observing is normal SLURM behavior - multiple jobs can share the same node unless you explicitly request exclusive access. This is actually efficient resource utilization, but if you need dedicated nodes for each job, use the --exclusive
flag or specify resource requirements that effectively claim the entire node.
Sources

Slurm guide for multiple queue mode - AWS ParallelCluster 

Slurm dynamic node allocation strategies in version 3.7.x - AWS ParallelCluster 

Slurm dynamic node allocation strategies in version 3.6.x and previous - AWS ParallelCluster 

Slurm guide for multiple queue mode - AWS ParallelCluster 

Slurm cluster fast insufficient capacity fail-over - AWS ParallelCluster 

Slurm memory-based scheduling - AWS ParallelCluster 

Examples - AWS ParallelCluster 

Slurm dynamic node allocation strategies in version 3.8.0 - AWS ParallelCluster 
