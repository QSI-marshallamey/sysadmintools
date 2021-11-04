instance-id: 'i-5e171171'
ami-id: 'ami-0e868466'
az: 'us-east-1e'
root-device-name: '/dev/sda1'
volume-id: 'vol-32a4697c'

{
    "ImageId": "ami-0f92ea0128e46ac20"
}

removed old hf-admin key pair
create new hf-admin key pair
aws ec2 create-key-pair --key-name AWS-Keypair --query "KeyMaterial" 
                        --output text > "C:\AWS\AWS_Keypair.pem"
aws ec2 create-image --no-reboot --name openVPN-old --instance-id i-5e171171
aws ec2 run-instances --image-id "ami-037ff6453f0855c46" --count 1 --instance-type t2.micro --key-name "hf-admin" --security-group-ids "sg-2cfadb48" --subnet-id "subnet-72cce448" --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=testVPN}]" --associate-public-ip-address

aws ec2 detach-volume --volume-id vol-32a4697c
aws ec2 attach-volume --device /dev/sda1 --instance-id <<>> --volume-id vol-32a4697c

aws ec2 detach-volume --volume-id vol-32a4697c
aws ec2 attach-volume --device /dev/sda1 --instance-id i-5e171171 --volume-id vol-32a4697c


OFFICIAL OPENVPN AMI: "ami-037ff6453f0855c46"

To connect to the VPN server: ssh -i hf-admin.pem openvpnas@52.7.59.138