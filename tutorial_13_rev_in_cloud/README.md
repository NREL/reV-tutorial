reV in the Cloud
===

The Renewable Energy Potential Model (reV) was originally designed to run on National Laboratory of the Rockies (NLR) High Performance Computer systems (HPCs) and access energy resource data on a local file system. Users wishing to run large-scale reV jobs without access to NLR's HPC can now recreate the original work flow using an [Amazon Web Services (AWS) Parallel Cluster](https://aws.amazon.com/hpc/parallelcluster/) to provide the compute infrastructure and the [Highly Scalable Data Service (HSDS)](https://www.hdfgroup.org/solutions/highly-scalable-data-service-hsds/) to provide access to resource data. This document will walk you through how to set these services up and start using large-scale reV in the cloud.

This guide is designed to provide both a step-by-step guide and detailed explanations for the basic components of a reV environment on an AWS Parallel Cluster and is oriented towards analysts with moderate to intermediate levels of experience with AWS. More experienced cloud architects may be interested in this Terraform-based guide produced by Switchbox: [https://github.com/switchbox-data/rev-parallel-cluster](https://github.com/switchbox-data/rev-parallel-cluster).

## 1) Setup an AWS Account
- Write for an audience that ranges from a non-CS University Grad Student to Upper/Intermediate-level IT professional. We don't really need to worry about AWS pros.
- We'll want a section on how to do this for both individual and institutional accounts. 
- Describe the Single Sign On Issue and reiterate the need for an IAM user.
    - Here we can probably contact John Readey to see if he found any insights into the Authorization protocol problem with SSO vs IAM user accounts

- From Whiteside:
> A lot of companies will just use IAM users and currently that will just work.  Others might use identify center and AWS SSO users, or other forms of SSO that use STS credentials.  We could stop here and just say SSO (STS credentials) doesn't work, you will need an IAM user account.  We could also look at hsds and see if we can fix it, it might be an easy fix to enable the use of STS credentials.


## 2) Install AWS Command Line Interfaces
Many of the instructions that follow will utilize AWS command line interfaces (CLIs). Full instructions for installing and using AWS CLIs can be found in the official Amazon page here: [https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html). To install these programs any user may download the installers from AWS's website [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), Unix users may use their OS's package manager (i.e., brew, apt, dnf, yum, etc), or you may create a virtual Python environment and install using `pip` or any other Python package manager, e.g.,:

```bash
python3 -m venv ~/envs/aws
source activate ~/envs/aws/bin/activate
pip install awscli aws-parallelcluster
```

Once you have installed these two programs, you then need to link them to your AWS account with a profile. The easiest way to do this is to run the `aws configure` command and follow the prompts to build a profile configuration file, which will be stored in a hidden AWS directory in your home folder (`~/.aws`). Before running this command, make sure you know your access key ID, secret access key, and target AWS region. We will default to JSON for the output format prompt. The resulting file will look like this:

Single-Sign On:
```yaml
[profile profile_name]
sso_session = account_name
sso_account_id = ************
sso_role_name = developers
region = us-west-2
output = json

[sso-session account_name]
sso_start_url = https://org-name.awsapps.com/start/#
sso_region = us-west-2
sso_registration_scopes = sso:account:access
```

Identity and Access Management (IAM):
```yaml
Include IAM case here
```

Moving forward, we need to tell the AWS CLI which profile to use for authentication. You may do this manually for each session by setting the `AWS_PROFILE` environment variable to this name in each comand-line session, you may specify the name in a `--profile` option for each CLI command, or you may add the variable to your command-line interpreter's startup script to automate this step, which is what we're suggesting for convenience. Here, we are using a Bash shell so will be editing the `~/.bashrc` script (Linux) or the `~/.bash_profile` (MacOS) to add the following line:

```bash
export AWS_PROFILE=profile_name
```

## 3) Configure SSH Access

The most direct way to interact with your parallel cluster is through a Secure Shell (SSH) Protocol connection. This will enable to you to both interact with the operating and file systems and to transfer data to and from the cluster. Because subsequent setup steps will require SSH information, it is best to go ahead and address this one before moving on. To do this, assuming you don't have existing keys stored on your computer, you first need to generate a pair (public and private) of SSH keys. There are a few ways to do this, outlined below.

> Note: While the most common of these algorithms (the Rivest–Shamir–Adleman crytosystem or `RSA`) will work for some operating systems, other images on AWS do not allow it and will require you to use a more up-to-date algorithm. In this case, you may use the newer `Ed25519` option, which is based on the Edwards-curve Digital Signature Algorithm. For more on AWS and SSH, see: [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html).


#### Method #1: Generate a key-pair on your local machine and copy the public key to AWS's Secrets manager
Users on Unix systems may use the built-in `ssh-keygen` command. Windows users may also use this command, though it will require the installation of an OpenSSH server. There are different algorithms and keysizes that you may specify when running this command and which one will be acceptable for your parallel cluster will depend on the security requirements of the operating system you chose when creating it. Here, given the limitations on some operatings systems described above, we will generate a Ed25519 key pair with the following command:

```
ssh-keygen -t ed25519
```

You will be prompted to enter a file in which to save the key pair. You may enter a file path if you wish, or you may just push enter to place your keys in the default location (`~/.ssh/id_ed25519` for Unix systems). Then you will be prompted to enter a passphrase, which is optional but protects you in cases where your private key is compromised. So, you may either use a passphrase or you may push enter for this prompt and the subsequent passphrase verification step to avoid having to enter the phrase each time you SSH into your cluster.

Following this step, assuming you used the default location, you will find your private key (`id_ed25519`) and public key (`id_25519.pub`) in the hidden `~/.ssh` directory. Open your EC2 portal (search for this in the search bar on the top of the page to the right on the AWS icon) and under "Network & Security" click the "Key Pairs" option. On the top right of this page, you'll find a blue "Actions" button with a dropdown option, use that to navigate to the "Import key pair" page. Give your key a name and either click the browse button to upload your public  key contents or paste the contents directly into the box below this option. Remember this key name, you'll need it when configuring your cluster. Once this is done, click the orange "Import key pair" to the bottom-right and you're done.

#### Method #2: Generate a key-pair through AWS Key Manager and copy the public key to your local machine
To use AWS to generate a key pair for you, navigate to the same "Key Pairs" page from your EC2 portal, but click the orange "Create key pair" button instead. You will be asked to give the key pair a name, as before, to choose both the encryption algorithm (RSA or ED25519), and to choose the private key format type. Assuming you are using an OpenSSH server, as described thus far, choose the `.pem` extension and click the orange "Create key pair" button at the bottom right. You will see a download screen pop up. Navigate to the location on your file system where'd you like to store the key file. We would suggest the default `~/.ssh` directory, but be careful not to overwrite any existing keys. Once you've finished this step you are done. 

#### Method #3: Generate a key-pair on your local machine and copy the public key to AWS
The AWS CLI provides an option to import a key pair directly from your terminal. To do this, follow the steps outlined in `Method #1`, but instead of importing your private key in the browser, run the following command:

```Bash
aws ec2 import-key-pair --key-name "your-key-name" --public-key-material "~/.ssh/ed_25519.pub"  # Or wherever you put the public key
```

For more information on this method, see
[https://docs.aws.amazon.com/cli/latest/reference/ec2/import-key-pair.html](https://docs.aws.amazon.com/cli/latest/reference/ec2/import-key-pair.html)


## 3) Setup and Deploy the Parallel Cluster
An AWS Parallel Cluster provides the user a head node that controls the distribution of computational work to a number of compute nodes, each of which are spun up on demand and shutdown after the work is finished. For reV runs, this also requires a shared file system. Once an AWS account is created, the user is able to choose the type of cluster they want and parameterize its characteristics. The following outlines how to configure and spin up a cluster using the AWS CLI, after which you will have access to the head node and file system until you delete the cluster (as outlined in [step 7](#7-aws-pcluster-clean-up)).


### 3a) The Parallel Cluster Configuration File

The next step is to write a YAML configuration file that specifies the build characteristic of the machines and software you wish to wish to deploy (e.g., operating system, disk, RAM, CPUs, job scheduler, etc.). Here, you may use the AWS CLI for a set of command lines prompts that will guide the build process or you may write your own manually. To use the guided process, use the command below or go to [The AWS Parallel Cluster Configuration page](https://docs.aws.amazon.com/parallelcluster/latest/ug/install-v3-configuring.html) for more detailed instructions.

```bash
pcluster configure --config "./cluster-config.yaml
```

To write your own configuration file, you may start with the [example configuration file](https://github.com/NREL/reV-tutorial/blob/master/tutorial_13_rev_in_cloud/rev-pcluster-config.yaml) provided for you in this repository. Each configuration section used in the example is briefly described below along with some notes on reV-specific considerations. For more information on how to specify your cluster to your needs please visit the latest [AWS documentation](https://docs.aws.amazon.com/parallelcluster/latest/ug/cluster-configuration-file-v3.html) and take a look at some AWS-provided [example configuration files](https://github.com/aws/aws-parallelcluster/tree/release-3.0/cli/tests/pcluster/example_configs).

1. **Region**:

    This is a top-level entry specifying the region of the data center that holds your cluster's hardware. See Amazon's Global Infrastructure page for a map showing all regions [here](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/). We suggest that you use "us-west-2", which is in Oregon, to reduce data transfer latency in the reV generation step (this is where the NLR resource data is stored). 

2. **Image**:

    This section provides an `Os` option for specifying the operating system (OS) you wish to use. The following Linux operating systems are supported in all regions (see [https://docs.aws.amazon.com/parallelcluster/latest/ug/Image-v3.html](https://docs.aws.amazon.com/parallelcluster/latest/ug/Image-v3.html)). We chose Ubuntu 24.04 in the example configuration because the `HSDS` package is tested on it, but other options may be more suitable depending on your comfort levels with the different Linux options or your institutions setup. Do note that different operating systems use different package managers, so that will affect the contents of the Bash script used to connect reV to the HSDS-stored resource data as described in [section 5](#5-configuring-rev).

    - `alinux2`: Amazon Linux 2
    - `alinux2023`: Amazon Linux 2023
    - `ubuntu2004`: Ubuntu 20.04 LTS
    - `ubuntu2204`: Ubuntu 22.04 LTS
    - `ubuntu2404`: Ubuntu 24.04 LTS
    - `rhel8`: Red Hat Enterprise Linux (RHEL) 8
    - `rhel9`: Red Hat Enterprise Linux (RHEL) 9
        > Note that RHEL systems will require registration with an "entitlement server". If you or your organization does not have a RHEL license, you will not be able to install required dependencies with the RHEL package manager (yum). Also, as per the methodology outlined in this guide, you will also need nough licenses to install HSDS and docker on each compute you check out. Because of this, RHEL is not recommended for users without access to RHEL licenses.

3. **HeadNode**

    This section describes the hardware and behavior of the "head" node, which is very similar to the "login" node many HPC users are likely accustomed to. This node does not need the highest performing hardware in your cluster. It only requires needs enough power to allow the user to comfortably navigate the file system, move files around, and to provide reV enough computational resource to efficiently submit jobs to the compute node. The hardware chosen in this example configuration (`t3.large`) is a general purpose, low-cost option with 2 virtual CPUs and 8 GiB of memory. This is "burstable" class of EC2 resources, which charges based on usage and is perfect for a reV head node setup with only periodic file editing and job submission activity. See the Amazon documentation for the [T3 EC2 Instance Class](https://aws.amazon.com/ec2/instance-types/t3/) for more information about this component.

    > Note that this section is also where you will specify the name of the SSH key-pair you created in [section 3](#3-configure-ssh-access). This entry is found in the `Ssh` subsection (`KeyName`).
    
    > Make sure to replace the `SubnetId` value in the `Networking` subsection with the appropriate value given to you by your system administrator or (where would you find this?)

    > Note that we are using read-only access for S3 buckets in this configuration (`AmazonS3ReadOnlyAccess`). This is because we are writing our reV outputs to the shared file system and only use S3 to access the resource data. If, for any reason, you need to elevate or refine your access privileges, change the `AdditionalIamPolicies` `Policy` entries to something more permissable. You may also add additional policies to fit your needs. See all available options here: [https://docs.aws.amazon.com/aws-managed-policy/latest/reference/policy-list.html](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/policy-list.html).

4. **Scheduling**

    A job scheduler is used to distribute computational work to the compute nodes and monitor usage. For multi-user setups, it also handles and prioritizes user requests for resources in a job "queue". This configuration section allows the user to both specify the job scheduler and each compute node that will be managed by that scheduler. In the example setup, the Slurm (originally, an acronym for Simple Linux Utility for Resource Management) job scheduler was used. The AWS Batch scheduler is also available, though this choice will change the configuration parameters needed and is only available on Amazon Linux images. In this section you'll see two different `SlurmQueues` entries; these are two SLURM-managed compute nodes used for different scale reV runs. The first we're calling the `standard` node and it uses a `c6a.12xlarge` EC2 instance. This is a moderately sized setup (48 CPUs, 96 GiB RAM) based on the 3rd generation AMD EPYC processors, which were originally released in 2021 and are suitable for standard reV wind and solar runs at a national scale (i.e., the Contiguous United States). See the AWS entry for the c6a EC2 class [here](https://aws.amazon.com/ec2/instance-types/c6a/). The second entry in the sample config is called the `bigmem` node and uses an m6a.12xlarge EC2 instance which provides 48 EPYC vCPUs as well but increases the available memory to 192 GiB (see [its AWS page here](https://aws.amazon.com/ec2/instance-types/c6a/)). These nodes are more useful for the memory-intensive reV-Bespoke module, which dynamically places individual turbines based on available land, wind resource, and wake losses. The appropriate instance type for your purpose will depend on many factors such as the scale of your reV runs, which modules you wish to use, your budget, etc. 
        
    Detailed information about all options in this section may be found [in AWS Parallel Cluster Scheduling page](https://docs.aws.amazon.com/parallelcluster/latest/ug/Scheduling-v3.html).

5. **SharedStorage**

    The final hardware component in the sample Parallel Cluster configuration file specifies disk and file system settings. reV is highly I/O intensive, relying heavily on the file system to write out temporary chunked files from compute nodes or to read in outputs from previous modules into subsequent modules in the modeling pipeline. Here, we have chosen a solid-state drive (SSD) Lustre file system mounted on `/scratch` with 1.2 TB of storage.  We have found that model performance for large-scale reV runs can be severely hampered by sub-optimal file systems and suggest that you stick with this option, though disk size and mount points will, of course, depend on your use-case. More information on this type of filesystem can be found in [AWS's Fsx for Lustre Documentation Page](aws.amazon.com/fsx/lustre/) and more configuration options for this entry in this configuration file can be found on [AWS's SharedStorage page](https://docs.aws.amazon.com/parallelcluster/latest/ug/SharedStorage-v3.html).

6. **Tags**

    The `Tags` section in the configuration file specifies options for resource management in CloudFormation. It is used in the sample config simply to communicate billing information, but may be used for many other management purposes. To learn more about this section, you may start at the [Parallel Cluster Tag Configuration page](https://docs.aws.amazon.com/parallelcluster/latest/ug/Tags-v3.html), which will then direct you to more resources describing CloudFormation and its options. 



### 3b) Spin Up Cluster

Before you can access your AWS account to create the parallel cluster we configured in [section 2b](2b-configure-cluster) we need to authenticate the connection. To do this, run the appropriate AWS sign-on command using the AWS CLI. For the single sign-on method use:

```bash
sso login
```

or, if you didn't set the `AWS_PROFILE` environment variable:

```
aws sso login --profile=profile_name
```

- *Include IAM case here*

Now we can use the `aws-parallelcluster` CLI to create your cluster. Run the following command (if you want to keep default cluster name from the sample config, you may use this command directly, otherwise update the cluster name to your own):

    `pcluster create-cluster -c rev-pcluster-config.yaml --cluster-name rev-pcluster`

If everything was configured correctly, you will see an output JSON message in your shell indicating that the creation process has begun (look for "CREATE_IN_PROGRESS"). This process will take some time to finish, but you may check on it's progress throught the EC2 CloudFormation portal in your AWS developers page where you'll see the status of each individual cluster component. You may also run the following command to see its overall status:

```
pcluster list-clusters
```

### 3c) Access Cluster

Now that you have a running cluster and an SSH key pair, you may log in to your head node, but you need two more items. First, you need to locate the hostname (or private IP address) associated with this instance. The easiest way to do this is to use the AWS CLI to "describe" your instance and locate the appropriate entry in the response. The response is a large JSON dictionary of information and the IP address is present in several locations. You may use just the `aws ec2 describe-instances` command and find the "PrivateIpAddress" entry manually, or you may use something like the following command to filter the response down to a single line representing the address:

```bash
aws ec2 describe-instances | grep PrivateIpAddress | tail -1 | awk '{print $2}'
```

Next, you'll need the username for the server. It is possible to add new user names to your instances (see, [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/managing-users.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/managing-users.html)), but since we have not described that step here, you will likely need to use the default user for the OS you chose in the image configuration step. Below are the default user names associated with the three OS groups described in [section 2b](#2b-configure-cluster) but you can find all default names in the "managing users" link above:

- **Amazon Linux**: *ec2-user*
- **RHEL**: *ec2-user* or *root*
- **Ubuntu**: *ubuntu*

Now we'll use the `ssh` command with the public key, username, and IP address (or "hostname") to connect to the clusters head node. This command can be saved as an alias for quick terminal access or used to connect the instance to an Integrated Development Environment (IDE) such as Visual Studio Code (VSCode). VSCode is a popular IDE for activities such as this and is how this team put together the sample runs used to develop this guide; for instructions on how to connect to your head node through VSCode see [https://code.visualstudio.com/docs/remote/ssh](https://code.visualstudio.com/docs/remote/ssh).

```bash
ssh -i ~/.ssh/publickey.pub user@hostname
```

> Note: If you have created and destroyed several AWS Parallel Clusters trying to get this to work, you may encounter some connection issues associated with SSH. If this happens, try removing entries for previous attempts (lines starting with the hostname or IP address) from the `~/.ssh/known_hosts` file.


## 4) Differences with an HPC
At this point, it is worthwhile to point out that there are default behaviors in an AWS Parallel Cluster that may differ from what an user with access to an onsite HPC might expect. This can cause some confusion when configuring a reV job since the model was designed specifically to run on NLR HPC systems.

On NLR's HPC, Slurm's exclusive node access option is turned on. If you submit a job to a compute node, that job has exclusive access to the entire server (i.e., all cpus and available memory). If you submit a second job, that job will check out a second compute node and block all those resources from other jobs submitted through the scheduler. So, this is the assumption that reV makes. This is more appropriate for HPC systems to prevent multiple users from interfering with each other's jobs.

AWS, however, uses the default SLURM settings and shares nodes between jobs by default. When you submit that second job, if there are still enough resources available on the first compute node, it will kick that job off on it. As you kick more jobs off, it will continue using that first node until it runs out of CPUs and/or memory after which the scheduler will spin up a second node and start kicking jobs off on that one. So, this make sense from an efficiency/cost perspective and gets around underutilization problems that can occur with exclusive node scheduling behavior, but it requires you to think differently about your execution control in reV configurations if you're used to this default behavior.

Alternatively, you can tweak a few settings to effectively turn node sharing off. Without having to spin up a new cluster, you may simply set the `memory` option in the reV `execution_control` block to approximately match the available memory on the target compute node. If you want to change the default behavior to be exclusive, you may add `JobExclusiveAllocation = true` to the target SLURM Queue (e.g., standard or bigmem in the example) in your AWS Parallel Cluster configuration file before spinning up your cluster. You may also specify the exclusive node option using the `feature` option in your `execution_control` block by setting the value to `--exclusive`.

Another subtle difference between NLR's Slurm setting and the default parameters used in AWS involves checking out an interactive node. The `salloc` command allows you to manually check out a compute node of your choosing. This may be useful if you wish to monitor a reV job mid-stream or if you'd like to check something like memory overhead before kicking your jobs off. On NLR's HPC systems, this will put you in a resource queue which can take more or less time to get through depending on how many other users are attempting to connect to the same compute nodes on the system. On high-traffic days, this may take a signficant amount of time depending on your node choice, how long you asked to use the resource, and how many other users are trying to checkout the same type of node. On low-traffic days, you may be instantly granted a compute node allocation and will be SSH'd into that node automatically. On an AWS system with default Slurm settings you will not necessarily have to wait for other users, but it will take some time for the node to spin up since these instances aren't on standby as they are on an HPC system. Then, once the node is ready, you will then have to manually log into that node. In this case, you may use the `squeue` command to see the hostname of the machine you checked out and then you can use the `ssh` command to log into it. Slurm settings such as this may be configured to your liking in the [Job Scheduler Section](docs.aws.amazon.com/parallelcluster/latest/ug/Scheduling-v3.html#yaml-Scheduling-Scheduler) of your Parallel Cluster configuration file.

## 5) Setup HSDS Server
HSDS can be used to access wind, solar, and other resource data that NLR houses in an AWS S3 bucket. For smaller, single node jobs, this can be done by installing HSDS, giving it access information to this S3 bucket, kicking it off directly on your file system, adjusting your resource file paths in your reV configs, and then letting reV handle the rest. However, since you went through all the trouble to setup your AWS account and spin up a parallel cluster, you're probably not running a small job. For large jobs, running an non-containerized HSDS server will likely encounter connection issues at some point and kill your reV runs. This problem can be largely fixed using HSDS Docker images. The current recommended approach for handling this is to write a script that will install HSDS, Docker, and kick off a containerized HSDS service on each compute node that a reV job uses. The following will walk you through setting up that process.

### 5a) Create Virtual Python Environment

The first step is to create a virtual Python environment that will contain both the reV model and HSDS Python APIs. There are many ways to do this, but this simplest is to use Python's builtin virtual environment module, `venv`. You can use the existing Python interpreter on your system or you can update it with your package manager, but make sure that the Python versions you're working with are compatible with reV. If you choose to use `venv`, you may need to install this module with your package manager. On our Ubuntu system, if you have Python 3.12, that command would be:

```bash
sudo apt install python3.12-venv
```

Then, create and activate this environment using a set of commands like this:

```bash
mkdir ~/envs
cd ~/envs
python3 -m venv rev
source rev/bin/activate
```

Then you could assign the activation command to an alias if you don't want to type it out each time with a command like this:

```bash
echo -e "\nalias arev='source ~/envs/rev/bin/activate'" >> ~/.bashrc
source ~/.bashrc
arev
```
> Note: This is the same environment you will install reV into. Perform this step before installing reV so that it doesn't point the interpreter away from this local `hsds` installation.


### 5b) Install HSDS
The HSDS repository has a number of useful scripts for Dockerizing a server. Clone this repository somewhere on your file system. Then use a 

```bash
git clone ~/https://github.com/HDFGroup/hsds.git
cd ~/hsds
python -m pip install . 
```

- IAM and authentication issues
- Kick off script


### 5c) Configure Data Access
1. Create an HSDS Configuration file in your home directory called `~/.hscfg` with the following content:
```
# Local HSDS server
hs_endpoint = http://localhost:5101
hs_username = admin
hs_password = admin
hs_api_key = None
hs_bucket = nrel-pds-hsds
```

2. Optionally, you can copy the password file and modify your username/password combinations:

```
cp ~/hsds/admin/config/passwd.default ~/hsds/admin/config/passwd.txt
```

2. Copy the start_hsds.sh script from this example (source file) to your home directory in the pcluster login node (e.g. cp /shared/reV/examples/aws_pcluster/start_hsds.sh ~/).

3. Replace the following environment variables in start_hsds.sh with your values: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and BUCKET_NAME (note that you should use AWS keys from an IAM user with admin privileges and not your AWS console root user).

4. Test your HSDS local server config, do the following:

    - Run the start script: sh ~/start_hsds.sh
    - Run docker ps and verify that there are 4 or more HSDS services active (hsds_rangeget_1, hsds_sn_1, hsds_head_1, and an hsds_dn_* node for every available core)
    - Run hsinfo and verify that this doesn’t throw an error
    - Try running pip install h5pyd and then run the the h5pyd test (either the .py in this example or the h5pyd test snippet below).



### 5d) Setup Notes:

1) Be careful about defining your AWS and HSDS environment variables. These can be defined in many places and can result in unexpected behavior if they aren’t aligned. Some of those places include:

- The HSDS config: `~/.hscfg`
- Your `~/.bashrc` file or any other script it runs
- The `start_hsds.sh`" Bash script
- The parameter override configuration file (`~/hsds/admin/config/override.yml`)

2) The contents of your `start_hsds.sh` script for installing and starting Docker depends on which OS you’re using since it uses the package manager to do it. Different OSes uses different package managers. The sample file included in this repository use the Advanced Package Tool (APT), which is common to all Debian-based operating systems such as Ubuntu. If you aren't using a Debian-based OS, you'll need to edit the file.



## 6) Setup reV

## 6a) Install reV and configuration files
- Navigate to the shared filesystem directory (since this is where we will be writing outputs) and clone this repository to get the sample reV configuration files and HSDS startup scripts. Then, in the same Python environment you installed HSDS into, install reV through PyPI, and run the CLI to check that it works:

```bash
cd /scratch/
git clone https://github.com/NREL/reV-tutorial.git
cd reV-tutorial/tutorial_13_rev_in_cloud/
pip install NREL-reV
reV
```

If you see reV's help file, the installation was successful and works on your system. In this folder you will see several "start_hsds" scripts

## 6b) Configure reV
There are at least two steps in a full reV model pipeline where reV will make a call to the resource data:

1) Generation: will always require access to resource data
2) Aggregation: will require access to resource data if a `techmap` has not been computed and saved to the exclusion file yet.

- The `sh_script` option points to a script that installs and kicks off HSDS on each compute node. If the run is not setup such that each SLURM node has full access to the compute node, this file will need to contain a lock to prevent multiple processes on the same server from attempting to install and run HSDS at the same time. This tutorial contains a few sample scripts that will achieve this, though the script may require adjustments depending on your operating system.

- reV Execution control:
    - When SLURM is not set to node sharing, there is more responsibility for the the user to ensure that each job is efficiently using its compute node. This can be done with a combination of settings:

        - `sites_per_worker`: The number of concurrent process the CPU will run at a time. A higher `sites_per_worker` value requires more memory but will reduce slower I/O processes. If you are getting either low memory utilization or out-of-memory (OOM) errors you can adjust this variable up or down.
        - `max_workers`: The maximum number of CPU cores per node to split reV work across. A higher number of workers will increase the memory overhead used to manage concurrency. If you are getting either low memory utilization or OOM errors you can also adjust this variable up or down.
        - `memory_utilization_limit`: The percentage of available memory at which reV starts dumping data from memory onto disk. Because disk I/O is slower than memory transfers, it can improve runtimes to perform fewer I/O operations by holding more data in memory for longer. However, full memory utilization is not desired because of the possibility for brief memory spikes (either from reV itself or background processes) that can cause OOM errors. So, this number can be adjusted up to some percentage of total available memory that leaves enough room other processes. Note that this is memory utilization at which reV will start dumping data to disk, meaning actual memory use will continue to rise for a period after it starts the write process. So, it needs to be lower than the 100% and that will depend on the behavior of system (in the sample reV-generation config, this value was set to 70% but the actual memory use topped out at about 90%). The proper value will depend on many factors such as your hardware, operating system (OS), other reV execution control settings, and other processes running on the server.
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


Make sure this key-value pair is set in the execution_control block of the config_gen.json file: "sh_script": "sh ~/start_hsds.sh"

Add the following to config_gen.json: config_gen["execution_control"]["sh_script"] = "sh ~/start_hsds.sh" this will start the HSDS server on each compute node before running reV.

Set the resource file paths in config_gen.json to the appropriate file paths on HSDS: config_gen["resource_file"] = "/nrel/wtk/conus/wtk_conus_{}.h5" (the curly bracket will be filled in automatically by reV). To find the appropriate HSDS filepaths, see the instruction set here.

You should be good to go! The line in the generation config file makes reV run the start_hsds.sh script before running the reV job. The script will install docker and make sure one HSDS server is running per EC2 instance.



## 7) Monitoring AWS Parallel Cluster Usage and Costs
- Just a real brief overview of how to monitor usage and avoid cost overruns.

In this setup, there are four main sets of fees for running reV on an AWS Parallel Cluster:

    1) Constant hourly head node fees
    2) Intermittant hourly compute node fees
    3) Constant hourly and storage-based SLURM accounting fees
    4) Various other AWS programs that provide services such as DNS resolution, system monitoring, threat detection, etc.

https://aws.amazon.com/pcs/pricing/


## 8) AWS Parallel Cluster Clean Up
- Remove the PCluster
- Depending on settings, you may need to handle the file system separately
- Ways to keep as much infrastructure alive with as little cost as possible
    - "The minimal state"
- Etc.


## 9) Deprecated and Untested Methods
Some older methods may still work, though they are not covered in this guide.
- Kubernetes

Other methods have been tested and were found to be less than ideal for reV
- AWS Lamda Functions

## Scratch Notes on Deployment
Notes on deployment

- The official amazon recommendations are to use docker to install hsds. This is what Grant followed. On rhel systems, this would require you to register for an entitlement server. At NREL, the system admins responded that they only had so many RHEL licenses, enough for the head (login) node but not enough for all of the compute nodes. Why they want us to use docker over a basic docker installation is unknown to me.
- Next, I tried amazon linux 2, not knowing about amazon linux 2023. Here, the hsds installation failed because I was unable to install gcc 9
- AWS Linux Operating Systems:
    - https://docs.aws.amazon.com/systems-manager/latest/userguide/operating-systems-and-machine-types.html#prereqs-os-linux
- Ubuntu
    - Next I tried Ubuntu, 22.04 and 24.04, but it won’t allow RSA keys. This can be done in the EC2 portal under “Network & Security” and “Key Pairs” (e.g., https://us-west-2.console.aws.amazon.com/ec2/home?region=us-west-2#InstanceDetails:instanceId=i-00035fdba289b5f4f) 
- In the start_hsds.sh you need to get the instance ID and type of each node. There are two ways to do this depending on your Instance Meta Data Service (IMDS) Version:
    - IMDS v1: 
        *     curl http://169.254.169.254/latest/meta-data/instance-type
        *     curl http://169.254.169.254/latest/meta-data/instance-id
    * IMDS v2:
        * TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600”). # Get your token first
        * curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-type
        * curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id
- The start_hsds.sh method of installing docker depends on which OS you’re using. Edit the file to reflect this:
    - https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-docker.html 
- If you cloned the hsds repository anywhere else than ~/hsds, replace that path on line 65
- Docker compose is now a separate package and the installation commands will also depend on your OS. For Amazon Linux 2023:
    * sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-linux-$(uname -m) -o /usr/bin/docker-compose && sudo chmod 755 /usr/bin/docker-compose
    * Then, to call it, replace every “docker compose” with “docker-compose” in hsds/runall.sh in the hsds repository
- When you run hsds through docker, if you want to stop it, run the hsds/stopall.sh script, which is just running the runall.sh script with a stop option
- If you ran HSDS in the background without Docker or some container and you want to stop it, good luck. It spins up a coordinator process and another process for each hsds server node you request. Each of these are very resilient and hard to kill, so far the only thing that’s worked is rebooting.
- Be very careful about defining your AWS and HSDS environment variables. These can be defined in many places and can result in unexpected behavior if they aren’t aligned. Some of those places include:
    - 1) The HSDS config: ~/.hscfg]
    - 2) Your .bashrc or any other scripts it runs
    - 3) The start hsds script
    - 4) The parameter override config (~/hsds/admin/config/override.yml)
- In the current SLURM configuration, the compute node only shutdowns after the wall time is reached, not if the job fails.
    - This would require either better tuning of the wall time (but will waste a lot of resource time regardless) or reconfiguring SLURM to shutdown after the command sent by GAPs fails.
