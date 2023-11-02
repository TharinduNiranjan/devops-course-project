
## Installation Guideline

1. Download or clone the repository.

2. Generate ssh keys using ssh-keygen

    ```bash
           ssh-keygen -t rsa -b 2048
    ```
3. Copy **id_rsa.pub** file(< userhome >/.ssh directory) to the cloned/download directory as 
 **authorized_keys**
4. Build the docker image using the below command
    ```bash
        docker build -t ansibletask .
    ```
5. Start one container from the Docker image.
    ```bash
        docker run -d --name container1 ansibletask
    ```
6. Get its IP Address using the below command.
    ```bash
        docker exec container1 ifconfig
    ```
7. Add the IP address of **container1** to the **hosts** file in the cloned/download directory.

8. Run the ansible playbook.
    ```bash
       ansible-playbook ansibletask-playbook.yaml 
    ```
9. Copy the output(01), including the output of "uptime"
10. Re-run and get the uptime(02) again for the 2nd time.
11. Start the second container from the Docker image.
    ```bash
      docker run -d --name container2 ansibletask
    ```
12. Get its IP address using the below command.
    ```bash
      docker exec container2 ifconfig
    ```
13. Add the IP address of **container2** to the **hosts** file and **comment** previously added **host entry**.
14. Run the ansible playbook.
    ```bash
      ansible-playbook ansibletask-playbook.yaml
     ```
15. Copy the output(03), including the output of "uptime"
16. Re-run and get the uptime(04) again for the 2nd time. 

## Outputs

  
  ``` 
   O1- "uptime_output.stdout_lines": [
        " 20:23:27 up 4 days, 11 min,  0 users,  load average: 1.41, 1.42, 1.32" 
      ] 
  ```
  ```
   O2- "uptime_output.stdout_lines": [
        " 20:24:10 up 4 days, 12 min,  0 users,  load average: 2.15, 1.62, 1.39"
    ]
  ```
  ```
   O3- "uptime_output.stdout_lines": [
        " 20:25:22 up 4 days, 13 min,  0 users,  load average: 1.33, 1.51, 1.38"
    ]
  ```
  ```
   O4- "uptime_output.stdout_lines": [
        " 20:26:51 up 4 days, 14 min,  0 users,  load average: 1.74, 1.56, 1.40"
    ]
  ```
## Analyze
   Output of uptime command was expectedly displayed.
## Comments
1. Got errors when I tried to update git using ansible playbook. I had to change the Dockerfile by giving the sudoers access to the ssluser.

2. To avoid host key checking, I had to add host_key_checking=false into the ansible.cfg.

3. It was much easier to use separate ansible.cfg file and hosts file rather than using of default files in /etc/ansible location. 