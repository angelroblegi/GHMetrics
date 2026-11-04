<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.AspNetCore.OpenApi" Version="10.0.14" />
    <PackageReference Include="Microsoft.Data.SqlClient" Version="7.1.1" />
  </ItemGroup>

</Project>

AEL.Fanaia.NovedadVSP.API/AEL.Fanaia.NovedadVSP.API/AEL.Fanaia.NovedadVSP.API.csproj

name: $(date:yyyyMMdd)$(rev:.r)
jobs:
- job: Job_1
  displayName: Agent job 1
  pool:
    name: DEV
  steps:
  - checkout: self
    clean: true


  - task: NuGetAuthenticate@1
    inputs:
      nuGetServiceConnections: 'Feed_Transversales_Auditoria'


  - task: NuGetCommand@2
    displayName: 'NuGet restore solution'
    inputs:
      command: 'restore'
      restoreSolution: '**/AEL.FanaiaRecaudo.DAP.sln'
      feedsToUse: 'config'
      nugetConfigPath: 'Nuget/nugetonlyrestore.config'

  - task: SonarQubePrepare@5
    displayName: Prepare analysis on SonarQube
    inputs:
      SonarQube: 'Sonar Qube 8.3'
      scannerMode: 'MSBuild'
      projectKey: 'AEL.FanaiaRecaudo.DAP'
      projectName: 'AEL.FanaiaRecaudo.DAP'
      projectVersion: '$(Build.BuildNumber)_$(Build.SourceBranchName)'
      extraProperties: |
        sonar.scm.exclusions.disabled=true
        sonar.verbose=true
        sonar.scanner.opts=-Xmx2048m
        sonar.scm.provider=git
        sonar.inclusions=**/*.cs
        sonar.cpd.cross_project=false

  - task: VSBuild@1
    displayName: 'Build project'
    inputs:
      solution: '**/AEL.FanaiaRecaudo.DAP/AEL.FanaiaRecaudo.DAP.csproj'
      configuration: 'Release'
      msbuildArchitecture: 'x64'
      clean: true

  - task: SonarQubeAnalyze@5
    inputs:
      jdkversion: 'JAVA_HOME_17_X64'
  - task: SonarQubePublish@5
    inputs:
      pollingTimeoutSec: '500'
  - task: sonar-buildbreaker@8
    displayName: Break build on quality gate failure
    inputs:
      SonarQube: 'Sonar Qube 8.3'

  - task: PostBuildCleanup@3
    displayName: Clean Agent Directories


project key : NovedadVSP_API
