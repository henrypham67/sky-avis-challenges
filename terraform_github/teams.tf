provider "github" {
  token = var.pat
  owner = var.org
}

variable "pat" {
  type        = string
  sensitive   = true
  description = "Github Personal Access Token"
}

variable "org" {
  type        = string
  description = "Organization Name"
}

locals {
  members_csv = csvdecode(file("members.csv"))
  team_names  = [for key in keys(local.members_csv[0]) : key if key != "Username"]
}


resource "github_team" "teams" {
  for_each = toset(local.team_names)

  name = each.value
}

locals {
  teams_name__id = {
    for team in github_team.teams : team.name => team.id
  }
  team__member = flatten([
    for row in local.members_csv : [
      for k, v in row : {
        team_id  = local.teams_name__id[k]
        username = row["Username"]
        role     = v
      } if k != "Username" && v != ""
    ]
  ])
}

output "teams" {
  value = local.team__member
}

resource "github_team_membership" "members" {
  depends_on = [github_team.teams]
  for_each   = { for membership in local.team__member : membership.username => membership }

  team_id  = each.value.team_id
  username = each.value.username
  role     = each.value.role
}
