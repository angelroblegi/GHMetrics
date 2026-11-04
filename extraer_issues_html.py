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
      projects: '**/**.slnx'
      feedsToUse: 'select'
      includeNuGetOrg: true

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
        sonar.cs.opencover.reportsPaths=$(System.DefaultWorkingDirectory)/TestResults/**/coverage.opencover.xml

  - task: DotNetCoreCLI@2
    displayName: Build project
    inputs:
      command: 'build'
      projects: '**/AEL.Fanaia.NovedadVSP.API/AEL.Fanaia.NovedadVSP.API.csproj'
      arguments: '--configuration Release --no-restore'

  - task: PowerShell@2
    displayName: 'Clean previous TestResults'
    inputs:
      targetType: 'inline'
      script: 'Remove-Item "$(System.DefaultWorkingDirectory)/TestResults*" -Recurse -Force -ErrorAction SilentlyContinue'

  - task: DotNetCoreCLI@2
    displayName: 'Ejecutar pruebas unitarias con cobertura'
    inputs:
      command: 'test'
      projects: '**/AEL.Fanaia.NovedadVSP.API.Tests/AEL.Fanaia.NovedadVSP.API.Tests.csproj'
      arguments: '--configuration Release --no-restore --logger trx --collect:"XPlat Code Coverage;Format=opencover" --results-directory $(System.DefaultWorkingDirectory)/TestResults'
      publishTestResults: false

  - task: PublishTestResults@2
    displayName: 'Publish Test Results'
    condition: succeededOrFailed()
    inputs:
      testResultsFormat: 'VSTest'
      testResultsFiles: '**/*.trx'
      searchFolder: '$(System.DefaultWorkingDirectory)/TestResults'

  - task: PublishCodeCoverageResults@2
    displayName: 'Publish Code Coverage'
    condition: succeededOrFailed()
    inputs:
      summaryFileLocation: '$(System.DefaultWorkingDirectory)/TestResults/**/coverage.opencover.xml'

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
