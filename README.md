# Sky Mavis challenge solutions

see challenges [here](./challenges.md)

for the challenge 1 and 2 if you don't have Python on your computer, you can use the Dockerfile that I putted in each
folder

## Challenge 1: NAT Allocator

```bash
docker build -t nat-allocator ./allocate_subnets

docker run --rm nat-allocator
```

## Challenge 2: HTTP SD exporter

```bash
docker build -t httpd_exporter ./httpd_sd

docker run --rm -p 5000:5000 --name httpd_exporter -d httpd_exporter

curl localhost:5000/probe

curl localhost:5000/metrics
```

## Challenge 3: Manage GitHub Team with Terraform

### Prerequisites

- GitHub Personal Access Token, for more information [how to create PAT](https://docs.github.com/en/enterprise-server@3.9/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token) and remember to set `admin:org` permission for the token
- GitHub Organization with invited members
- Update the `members.csv` file with the actual team names and memeber names

### How to run 

```bash
terraform init

terraform plan --var 'pat=<Your GitHub Personal Access Token>' --var 'org=<Your Organization Name>'

terraform apply --var 'pat=<Your GitHub Personal Access Token>' --var 'org=<Your Organization Name>'
```