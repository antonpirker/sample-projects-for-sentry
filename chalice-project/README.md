# Chalice Sample Project

Chalice is a micro framework that helps setting up AWS Lambda functions written in Python.

# Getting started

# Install AWS CLI

Follow: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Configure AWS cli like described here: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html

# Deploying

Call `chalice deploy` in the `helloworld` directory and a new version will be deployed to AWS Lambda and a Link to the running service will be printed to stdout.

When multiple users want to deploy the same chalice app to the same AWS account they could configure differnt default regions in their AWS cli configuration and thus have separate versions of the function running in the same account.
