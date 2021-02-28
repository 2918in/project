from troposphere import (
 Export,
 Join,
 Output,
 Ref,
 Parameter,
 Template
)
from troposphere.ecr import Repository
t = Template()

t.set_description("gusiya-s3-repo")

t.add_parameter(Parameter(
 "RepoName",
 Type="String",
 Description="Name of repo"
))

t.add_resource(Repository(
 "Repository",
 RepositoryName=Ref("RepoName")
))

t.add_output(Output(
 "Repository",
 Description="Gusiya-container-repo",
 Value=Ref("RepoName"),
 Export=Export(Join("-", [ Ref("RepoName"), "repo"])),
))

print(t.to_json())
