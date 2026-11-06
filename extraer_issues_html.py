name: $(date:yyyyMMdd)$(rev:.r)
variables:
  solution: 'AEL.LogsBancarios.ActivarProceso.Function/AEL.LogsBancarios.ActivarProceso.Function.sln'
  projectPath: '$(Build.SourcesDirectory)/AEL.LogsBancarios.ActivarProceso.Function'
  sonarProject: 'AEL.LogsBancarios.ActivarProceso.Function'
  MSBUILDDISABLENODEREUSE: '1'
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

  - task: DotNetCoreCLI@2
    displayName: 'Restore NuGet Packages'
    inputs:
      command: 'restore'
      projects: '$(solution)'
      feedsToUse: 'select'
 
  - task: SonarQubePrepare@5
    displayName: Prepare analysis on SonarQube
    inputs:
      SonarQube: 'c920b15f-1de4-45cf-8de8-00186bd2439a'
      scannerMode: 'MSBuild'
      projectKey: '$(sonarProject)'
      projectName: '$(sonarProject)'
      projectVersion: '$(Build.BuildNumber)_$(Build.SourceBranchName)'
      extraProperties: |
        # Additional properties that will be passed to the scanner, 
        # Put one key=value per line, example:
        sonar.coverage.exclusions=AEL.LogsBancarios.ActivarProceso.Function/AEL.LogsBancarios.ActivarProceso.Function/Program.cs
        sonar.cs.opencover.reportsPaths=$(projectPath)/coverage.opencover.xml
        # Configuración de paralelismo
        sonar.parallel=true
        sonar.parallel.maxThreads=4
        # Optimización de memoria para el scanner
        sonar.scanner.opts=-Xmx2048m
        # Configuración para análisis incremental
        sonar.scm.provider=git
        
  - task: DotNetCoreCLI@2
    displayName: Build project
    inputs:
      command: 'build'
      projects: '$(solution)'
      arguments: '--configuration Release --no-restore'
      
  - task: DotNetCoreCLI@2
    displayName: 'Ejecutar pruebas unitarias con cobertura'
    enabled: True
    inputs:
      command: 'test'
      projects: '$(projectPath)/AEL.LogsBancarios.ActivarProceso.Tests/ActivarProcesoLogsBancariosFunctionTests.cs'
      arguments: '--configuration Release --no-build --collect:"XPlat Code Coverage" -- DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.Format=opencover'
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
