name: $(date:yyyyMMdd)$(rev:.r)
jobs:
- job: Phase_1
  displayName: Trabajo de agente 1
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
      projects: '**/**.sln'
      feedsToUse: 'select'
      
  - task: SonarQubePrepare@7
    displayName: Prepare Analysis SonarQube
    inputs:
      SonarQube: 'Sonar-NovedadesRefactor'
      scannerMode: 'dotnet'
      projectKey: 'NovedadVSP_API'
      projectName: 'NovedadVSP_API'
      projectVersion: '$(Build.BuildNumber)_$(Build.SourceBranchName)'
      extraProperties: |
        sonar.scm.exclusions.disabled=true
        sonar.scm.provider=git
        sonar.inclusions=**/*.cs
        sonar.cpd.cross_project=false

  - task: DotNetCoreCLI@2
    displayName: Build project
    inputs:
      command: 'build'
      projects: '**/AEL.Fanaia.NovedadVSP.API/AEL.Fanaia.NovedadVSP.API.csproj'
      arguments: '--configuration Release --no-restore'

  - task: SonarQubeAnalyze@7
    displayName: Run Code Analysis
    inputs:
      jdkversion: 'JAVA_HOME_17_X64'

  - task: SonarQubePublish@7
    displayName: Publish Quality Gate Result
    inputs:
      pollingTimeoutSec: '500'

  - task: sonar-buildbreaker@8
    displayName: Break build on quality gate failure
    inputs:
      SonarQube: 'Sonar-NovedadesRefactor'

  - task: PostBuildCleanup@3
    displayName: Clean Agent Directories
