#!/bin/bash

if [python -mplatform | grep -qi Ubuntu]; then
	echo "deb http://pkg.scaleft.com/deb linux main" | sudo tee -a /etc/apt/sources.list
	curl -C - https://dist.scaleft.com/pki/scaleft_deb_key.asc | sudo apt-key add - 
	sudo apt-get update 
	sudo apt-get install scaleft-server-tools -y
	sleep 5
	sudo touch /var/lib/sftd/enrollment.token
	echo eyJzIjoiMzI4NGU2OGUtNWM0ZC00NzA4LWI1ZGItYTA1Y2ZmYzUxNzVkIiwidSI6Imh0dHBzOi8vYXBwLnNjYWxlZnQuY29tIn0= | sudo tee -a /var/lib/sftd/enrollment.token

else
	sudo yum update -y
	curl -C - https://pkg.scaleft.com/scaleft_yum.repo | sudo tee /etc/yum.repos.d/scaleft.repo
	sudo rpm --import https://dist.scaleft.com/pki/scaleft_rpm_key.asc
	sudo yum install scaleft-server-tools -y
	sleep 5
	sudo touch /var/lib/sftd/enrollment.token
	echo eyJzIjoiMzI4NGU2OGUtNWM0ZC00NzA4LWI1ZGItYTA1Y2ZmYzUxNzVkIiwidSI6Imh0dHBzOi8vYXBwLnNjYWxlZnQuY29tIn0= | sudo tee -a /var/lib/sftd/enrollment.token
fi

