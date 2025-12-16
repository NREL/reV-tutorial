reV in the Cloud
===

The Renewable Energy Potential Model (reV) was originally designed to run on National Renewable Energy Laboratory (NREL) High Performance Computer systems (HPCs) and access energy resource data on a local file system. Users wishing to run large-scale reV jobs without access to NREL's HPC can recreate the original work flow using an [Amazon Web Services (AWS) Parallel Cluster](https://aws.amazon.com/hpc/parallelcluster/) to provide the compute infrastructure and the [Highly Scalable Data Service (HSDS)](https://www.hdfgroup.org/solutions/highly-scalable-data-service-hsds/) to provide access to resource data. This document will walk you through how to set these services up and start using reV in the cloud.


## 1) Setup an AWS Account
- Write for an audience that ranges from a non-CS University Grad Student to Upper Intermediate-level IT professional. We don't really need to worry about AWS pros.
- We'll want a section on how to do this for both individual and institutional accounts. 
- Describe the Single Sign On Issue and reiterate the need for an IAM user.
    - Here we can probably contact John Readey to see if he found any insights into the Authorization protocol problem with SSO vs IAM user accounts
- From Whiteside:
> A lot of companies will just use IAM users and currently that will just work.  Others might use identify center and AWS SSO users, or other forms of SSO that use STS credentials.  We could stop here and just say SSO (STS credentials) doesn't work, you will need an IAM user account.  We could also look at hsds and see if we can fix it, it might be an easy fix to enable the use of STS credentials.

## 2) Setup a Parallel Cluster
An AWS Parallel Cluster provides the user a head node that controls the distribution of computational work to compute nodes which are spun up on demand and shutdown after the work is finished.
- Discuss the different options for spinning up a cluster
    - AWS pcluster CLI
    - User interfaces
    - etc.
- Discuss the configuration file
    - The configuration file will require some elaboration.
 
## 3) Differences with an HPC
There are default behaviors in an AWS Parallel Cluster that may differ significantly from what an HPC user might expect. This can cause some confusion when configuring a reV job since the model was designed specifically to run on HPC systems.

On NREL's HPC, exclusive node access is turned on. If you submit a job to a compute node, that job has exclusive access to the entire server (i.e., all cpus and available memory). If you submit a second job, that job will check out a second compute node and block all those resources from other jobs submitted through the scheduler. So, this is the assumption that reV makes. This is important for message passing between nodes (MPI) and is more appropriate for HPC systems to prevent multiple users from interfering with each other's jobs.

AWS, however, uses the default SLURM settings and shares nodes between jobs by default. When you submit that second job, if there are still enough resources available on the first compute node, it will kick that job off on it. As you kick more jobs off, it will continue using that first node until it runs out of CPUs and/or memory after which the scheduler will spin up a second node and start kicking jobs off on that one. So, this make sense from an efficiency/cost perspective and gets around underutilization problems that can occur with exclusive node scheduling behavior, but it requires you to think differently about your execution control in reV configurations if you're used to this default behavior.

Alternatively, you can tweak a few settings to effectively turn node sharing off. Without having to spin up a new cluster, you may simply set the `memory` option in your `execution_control` block to approximately match the available memory on the target compute node (this actually didn't work, AI!). If you want to change the default behavior to be exclusive, you may add `JobExclusiveAllocation = true` to the target SLURM Queue in your AWS Parallel Cluster configuration file before spinning up your cluster.

## 4) Setup an HSDS Server
HSDS can be used to access wind, solar, and other resource data that NREL houses in an AWS S3 bucket. For smaller jobs single node jobs, this can be done by installing HSDS, giving it access information to this S3 bucket, kicking it off directly on your file system, adjusting your resource file paths in your reV configuration files, and then letting reV handle the rest. However, since you went through all the trouble to setup your AWS account and spin up a parallel cluster, you're probably not running a small job.

For large jobs, a local HSDS server will likely encounter connection issues at some point and kill your reV project. This problem can be largely fixed using Docker. Also, since you're spinning up multiple machines to distribute reV work, you'll need to install and kick off HSDS on each machine you spin up.

- Setting up Docker
- IAM and authentication issues
- Different pacakge managers for different OSs, some with caveats
- Kick off script
    - Exclusive vs node sharing (i.e., whether a file lock is needed)

## 5) Configuring reV
- The sh_script option points to a script that installs and kicks off HSDS on each compute node. If the run is not setup such that each SLURM node has full access to the compute node, this file will need to contain a lock to prevent multiple processes on the same server from attempting to install and run HSDS at the same time. This tutorial contains a few sample scripts that will achieve this, though the script may require adjustments depending on your operating system.
- reV Execution control:
    - When SLURM is not set to node sharing, there is more responsibility for the the user to ensure that each job is efficiently using its compute node. This can be done with a combination of settings:

        - `sites_per_worker`: The number of concurrent process the CPU will run at a time. A higher `sites_per_worker` require more memory but will reduce slower I/O processes. If you are getting either low memory utilization or out-of-memory (OOM) errors you can adjust this variable up or down.
        - `max_workers`: The maximum number of CPU cores per node to split reV work across. A higher number of workers will increase the memory overhead used to manage concurrency. If you are getting either low memory utilization or OOM errors you can also adjust this variable up or down.
        - `memory_utilization_limit`: The percentage of available memory at which reV starts dumping data from memory onto disk. Because disk I/O is slower than memory transfers, it can improve runtimes to perform fewer I/O operations by holding more data in memory for longer. However, full memory utilization is not desired because of the possibility for brief memory spikes (either rom reV or background processes) that can cause OOM errors. So, this number can be adjusted up to some percentage of total available memory that leaves enough room other processes. Note that this is memory utilization at which reV will start dumping data to disk, meaning actual memory use will continue to rise for a period after it starts the write process. So, it needs to be lower than the 100% and that will depend on the behavior of system (in the sample reV-generation config, this value was set to 70% but the actual memory use topped out at about 90%). The proper value will depend on many factors such as your hardware, operating system (OS), other reV execution control settings, and other processes running on the server.
        - `nodes`: The number of nodes you choose will determine the number of individual processes (reV sites) that each individual node runs. The larger number of nodes, the smaller number of sites. On a shared HPC system, a higher number of nodes could result in longer queue times, especially on busy days. More nodes will also result in longer node and process start up times and more chunked files written to the filesystem. More nodes will of course result in faster model runs according to your, but it could actually increase overall computational resource costs given the overhead mentioned above.
        - `pool_size`: placeholder
    - When SLURM is set to share nodes, additional resources left on any one node may be consumed with additional jobs. While this has the potential to improve efficiency, I have not experimented enough with this setup to describe it much detail or to make execution control suggestions.
- HSDS Configuration
    - HSDS has certain request limits that you may have to either account for or adjust to perform large-scale reV runs. Bascially, everything from line 32 to 60 falls into this group, but here are few to start:
        - `max_tcp_connections`: max number of inflight tcp connections?
        - `max_pending_write_requests`: maxium number of inflight write requests?
        - `max_task_count`: maximum number of concurrent tasks per node before server will return 503 error?**
        - `max_tasks_per_node_per_request`:  maximum number of inflight tasks to each node per request?
    - If you are struggling with Docker and HSDS, you might want to turn on timestamps in the HSDS config to help identify events. (I didnt' manage to get this to work, still no time stamps)
    - A common problem you might come across is a violation of the max HSDS task count settings. You are, by default, allowed 100 concurrent tasks per node. If you exceed this count, you will receive a 503 error. You can tell if this is the error by sshing into the offending node (e.g., `ssh standard-dy-standard-6`), using the docker logs command on the HSDS server node, and searching the output for 503 errors (`docker logs hsds_sn_1 | grep 503`). You can solve this by reducing the possible number of concurrent processes in the reV configuration file (e.g., reduce `max_workers`) or by adjusting the HSDS parameter in a `override.yaml` file in the HSDS repository (e.g., `~/github/hsds/admin/override.yml`). This override file will supercede individual entries in `config.yml` with user-supplied values. In our example problem, the `override.yml` file would contain only the line `max_task_count: <task count>` (e.g., `max_task_count: 150`). If you run enough sample reV runs, it will probably become clear whether this is a common problem that requires a more fundamental change to your execution control in reV or if it's rare enough that a slightly higher HSDS task count will be suffice. The default for this parameter is `100`.


6) Monitoring AWS PCluster usage and costs
- Just a real brief overview of how to monitor usage and avoid cost overruns.

7) AWS PCluster clean up
- Remove the PCluster
- Depending on settings, you may need to handle the file system separately
- Ways to keep as much infrastructure alive with as little cost as possible
    - "The minimal state"
- Etc.


## AWS Parallel Cost Service
In this setup, there are four main sets of fees for running reV on an AWS Parallel Cluster:

    1) Constant hourly head node fees
    2) Intermittant hourly compute node fees
    3) Constant hourly and storage-based SLURM accounting fees
    4) Various other AWS programs that provide services such as DNS resolution, system monitoring, threat detection, etc.

https://aws.amazon.com/pcs/pricing/
