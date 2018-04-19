# CloudComputing
CS 5412 Cloud Computing Project

## Deploy to EC2 Quick
Welcome to the world of automation. Get ready to be blown away :) 

### Running Local VM (for testing)
To get started we must install `Vagrant` [here](https://www.vagrantup.com/docs/installation/)

With vagrant installed: check success of installation with `vagrant help`

Next, you will install `ansible` which can be done with this command: `sudo pip install ansible`

Now you are ready to have some fun! Follow these steps exactly to deploy and test your app:

```bash
$ git clone https://github.com/chrisroman/CloudComputing.git
$ cd CloudComputing
$ cd vagrant
$ vagrant up
$ vagrant provision
...
TASK [Make sure nginx is running] **********************************************
ok: [default] => {"changed": false, "name": "nginx", "state": "started"}

RUNNING HANDLER [restart nginx] ************************************************
changed: [default] => {"changed": true, "name": "nginx", "state": "started"}

PLAY RECAP *********************************************************************
default                    : ok=16   changed=12   unreachable=0    failed=0
```

Now navigate to `http://192.168.33.10/` and you will see the app loaded up!

### Deploying to AWS
Let's deploy this AWS now! 

First step is to launch an EC2 instance

This EC2 instance should be using `Ubuntu Server 14.04 LTS (HVM), SSD Volume Type` as an AMI. 
This AMI will be the same type of OS that we used for our VM.

I would recommend that you choose the `t2.micro`, which is a small, free tier-eligible instance type. 

Make your security group one with these configs:

| Ports | Protocol | Source          |
|:-----:|:--------:|-----------------|
|   80  |    tcp   | 0.0.0.0/0, ::/0 |
|   22  |    tcp   | 0.0.0.0/0, ::/0 |
| 443   |    tcp   | 0.0.0.0/0, ::/0 |

After, launching download the the key-pair and name it `cloudcomputing`. 

Place the `cloudcomputing.pem` inside the vagrant folder. **DO NOT UPLOAD
THIS FILE TO ANYWHERE.**

Ensure, that your vagrant folder looks like this:

```bash
$ ls
Vagrantfile     cloudcomputing.pem   ansible.cfg     cs.nginx.j2     hosts           site.yml        upstart.conf.j2
$ chmod 700 cloudcomputing.pem
```

Your next step will be to take the public IP found when clicking on your instance in the EC2 terminal under: `IPv4 Public IP`
and putting that into the hosts file. So the hosts file should look like this, with <YOUR_PUBLIC_IP> being replaced by that `IPv4 Public IP` value:

```yml
[webservers]
 <YOUR_PUBLIC_IP> ansible_ssh_user=ubuntu
```

(*Not sure if this step is necessary*): Ensure that you had the private key by running `ssh-keygen`:

```bash
$ ssh-keygen 
enerating public/private rsa key pair.
Enter file in which to save the key (/Users/<YOUR_USERNAME>/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /Users/<YOUR_USERNAME>/.ssh/id_rsa.
Your public key has been saved in /Users/<YOUR_USERNAME>/.ssh/id_rsa.pub.
...
```

After this you are ready to push have an automated script push to your EC2 instance, just execute this:

```bash
$ ansible -m ping webservers --private-key=cloudcomputing.pem --inventory=hosts --user=ubuntu
<YOUR_PUBLIC_IP> | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
$ ansible-playbook -v site.yml
...
PLAY [Starting a Simple Flask App] ******************************************************************************************************************************************************************

TASK [Gathering Facts] ******************************************************************************************************************************************************************************
ok: [<YOUR_PUBLIC_IP>]
...
TASK [Make sure nginx is running] *******************************************************************************************************************************************************************
ok: [<YOUR_PUBLIC_IP>] => {"changed": false, "name": "nginx", "state": "started"}

PLAY RECAP ******************************************************************************************************************************************************************************************
<YOUR_PUBLIC_IP>             : ok=15   changed=2    unreachable=0    failed=0
```

For now, things don't exactly work. You will have to SSH into your EC2 instance
and manually start the upstart service (for some reason).
In your local terminal, run
```bash
$ ssh -i cloudcomputing.pem ubuntu@<Public DNS (IPv4) HERE>

$ sudo initctl start upstart
```

Boom! You are done :) How easy was that!
