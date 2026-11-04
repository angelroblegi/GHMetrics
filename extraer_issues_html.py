name: $(date:yyyyMMdd)$(rev:.r)
jobs:
- job: Job_1
  displayName: Agent job 1
  pool:
    name: DEV
  steps:
  - checkout: self
    clean: true

  - task: UseDotNet@2
    inputs:
        packageType: 'sdk'
        version: '10.x'

  - task: NuGetAuthenticate@1
    inputs:
      nuGetServiceConnections: 'Feed_Transversales_Auditoria'

  - task: DotNetCoreCLI@2
    displayName: 'Restore NuGet Packages'
    inputs:
      command: 'restore'
      projects: '**/AEL.Fanaia.NovedadVSP.API/AEL.Fanaia.NovedadVSP.API.csproj'
      feedsToUse: 'config'
      nugetConfigPath: 'nuget.config'

  - task: SonarQubePrepare@5
    displayName: Prepare analysis on SonarQube
    inputs:
      SonarQube: 'Sonar Qube 8.3'
      scannerMode: 'MSBuild'
      projectKey: 'NovedadVSP_API'
      projectName: 'NovedadVSP_API'
      projectVersion: '$(Build.BuildNumber)_$(Build.SourceBranchName)'
      extraProperties: |
        sonar.scm.exclusions.disabled=true
        sonar.verbose=true
        sonar.scanner.opts=-Xmx2048m
        sonar.scm.provider=git
        sonar.inclusions=**/*.cs
        sonar.cpd.cross_project=false

  - task: DotNetCoreCLI@2
    displayName: Build project
    inputs:
      command: 'build'
      projects: '**/AEL.Fanaia.NovedadVSP.API/AEL.Fanaia.NovedadVSP.API.csproj'
      arguments: '--configuration Release --no-restore'

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
