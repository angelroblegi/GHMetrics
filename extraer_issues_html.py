name: $(date:yyyyMMdd)$(rev:.r)
variables:
  solution: 'AEL.Administradora.CargueDatosBDReferencia/AEL.Administradora.CargueDatosBDReferencia.sln'
  projectPath: '$(Build.SourcesDirectory)/AEL.Administradora.CargueDatosBDReferencia'
  sonarProject: 'AEL.Administradora.CargueDatosBDRefencia'
jobs:
- job: Job_1
  displayName: Agent job 1
  pool:
    name: DEV
  steps:
  - checkout: self
    clean: true
  - task: DotNetCoreCLI@2
    displayName: 'Restore NuGet Packages'
    inputs:
      command: 'restore'
      projects: '**/**.sln'
      feedsToUse: 'select'

  - task: SonarQubePrepare@5
    displayName: Prepare analysis on SonarQube
    inputs:
      SonarQube: c920b15f-1de4-45cf-8de8-00186bd2439a
      scannerMode: 'MSBuild'
      projectKey: 'AEL.Administradora.CargueDatosBDReferencia'
      projectName: 'AEL.Administradora.CargueDatosBDReferencia'
      projectVersion: '$(Build.BuildNumber)_$(Build.SourceBranchName)'
      extraProperties: |
        sonar.exclusions=**/bin/**,**/obj/**
        sonar.coverage.exclusions=**/Program.cs,**/*.Test/**
        sonar.cs.opencover.reportsPaths=$(Agent.TempDirectory)/TestResults/**/coverage.opencover.xml
        sonar.scm.provider=git

  - task: DotNetCoreCLI@2
    displayName: Build project
    inputs:
      command: 'build'
      projects: '$(projectPath)/AEL.Administradora.CargueDatosBDReferencia/AEL.Administradora.CargueDatosBDReferencia.sln'
      arguments: '--configuration Release --no-restore'

  - task: DotNetCoreCLI@2
    displayName: 'Ejecutar pruebas unitarias con cobertura'
    enabled: True
    inputs:
      command: 'test'
      projects: '$(projectPath)/AEL.Administradora.CargueDatosBDReferencia.Test/AEL.Administradora.CargueDatosBDReferencia.Test.csproj'
      arguments: '--configuration Release --no-build --collect:"XPlat Code Coverage" --results-directory $(Agent.TempDirectory)/TestResults -- DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.Format=opencover'
      publishTestResults: true

  - task: SonarQubeAnalyze@5
    displayName: Run Code Analysis

  - task: SonarQubePublish@5
    displayName: Publish Quality Gate Result
    inputs:
      pollingTimeoutSec: 500

  - task: sonar-buildbreaker@8
    displayName: Break build on quality gate failure
    inputs:
      SonarQube: c920b15f-1de4-45cf-8de8-00186bd2439a

  - task: PostBuildCleanup@3
    displayName: Clean Agent Directories
