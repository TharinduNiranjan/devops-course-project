# Using Ubuntu base image
FROM ubuntu

# Install SSH for secure communication and other required softwares
RUN apt-get update && apt-get install -y openssh-server python3 sudo net-tools

# Creating ssluser for SSH access
RUN useradd -m -s /bin/bash -G sudo ssluser

# Set up SSH for key-based authentication
RUN mkdir -p /home/ssluser/.ssh
COPY authorized_keys /home/ssluser/.ssh/
RUN chown -R ssluser:ssluser /home/ssluser/.ssh
RUN chmod 700 /home/ssluser/.ssh
RUN chmod 600 /home/ssluser/.ssh/authorized_keys

# Add ssluser into sudoers.d folder
RUN echo 'ssluser ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/ssluser

# Start SSH service
ENTRYPOINT service ssh start && tail -f /dev/null
