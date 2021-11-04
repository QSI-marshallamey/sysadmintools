aws dynamodb create-table `
    --table-name family `
    --attribute-definitions `
        AttributeName=id,AttributeType=N `
        AttributeName=group,AttributeType=S `
    --key-schema `
        AttributeName=id,KeyType=HASH `
        AttributeName=group,KeyType=RANGE `
    --provisioned-throughput `
        ReadCapacityUnits=5,WriteCapacityUnits=5

aws dynamodb create-table `
    --table-name friends `
    --attribute-definitions `
        AttributeName=id,AttributeType=N `
        AttributeName=group,AttributeType=S `
    --key-schema `
        AttributeName=id,KeyType=HASH `
        AttributeName=group,KeyType=RANGE `
    --provisioned-throughput `
        ReadCapacityUnits=5,WriteCapacityUnits=5

aws dynamodb create-table `
    --table-name neighbors `
    --attribute-definitions `
        AttributeName=id,AttributeType=N `
        AttributeName=group,AttributeType=S `
    --key-schema `
        AttributeName=id,KeyType=HASH `
        AttributeName=group,KeyType=RANGE `
    --provisioned-throughput `
        ReadCapacityUnits=5,WriteCapacityUnits=5
    