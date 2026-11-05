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
    displayName: 'NuGet Authenticate'
    inputs:
      nuGetServiceConnections: 'Feed_Transversales_Auditoria, Feed_Transversales_ControlAcceso, Feed_Transversales_Notificaciones, Feed_Transversales_PasarelaPagos, Feed_Transversales_Personas, Feed_Transversales_TerminosCondiciones'

  - task: DotNetCoreCLI@2
    displayName: 'Restore NuGet Packages'
    inputs:
      command: 'restore'
      projects: 'AEL.ValidadorPropio.OmisosNovedad200.Function/AEL.ValidadorPropio.OmisosNovedad200.Function.sln'
      feedsToUse: 'select'

  - task: SonarQubePrepare@5
    inputs:
      SonarQube: 'Sonar Qube 8.3-Fanaia Administradora'
      scannerMode: 'CLI'
      configMode: 'manual'
      cliProjectKey: 'AEL.ValidadorPropio.OmisosNovedad200.Function'
      cliProjectName: 'AEL.ValidadorPropio.OmisosNovedad200.Function'
      cliProjectVersion: '$(Build.BuildNumber)_$(Build.SourceBranchName)'
      cliSources: '$(Build.SourcesDirectory)/AEL.ValidadorPropio.OmisosNovedad200.Function/'
      extraProperties: |
        # Additional properties that will be passed to the scanner, 
        # Put one key=value per line, example:
        sonar.coverage.exclusions=AEL.ValidadorPropio.OmisosNovedad200.Function/AEL.ValidadorPropio.OmisosNovedad200.Function/Program.cs
        sonar.cs.opencover.reportsPaths=$(Build.SourcesDirectory)/AEL.ValidadorPropio.OmisosNovedad200.Function/coverage.opencover.xml
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
      projects: '$(Build.SourcesDirectory)/AEL.ValidadorPropio.OmisosNovedad200.Function/AEL.ValidadorPropio.OmisosNovedad200.Function/AEL.ValidadorPropio.OmisosNovedad200.Function.csproj'
      arguments: '--configuration Release'


  - task: DotNetCoreCLI@2
    displayName: 'Ejecutar pruebas unitarias con cobertura'
    enabled: True
    inputs:
      command: 'test'
      projects: '$(Build.SourcesDirectory)/AEL.ValidadorPropio.OmisosNovedad200.Function/AEL.ValidadorPropio.OmisosNovedad200.Tests/AEL.ValidadorPropio.OmisosNovedad200.Tests.csproj'
      arguments: '--configuration Release /p:CollectCoverage=true /p:CoverletOutputFormat=opencover /p:CoverletOutput=$(Build.SourcesDirectory)/AEL.ValidadorPropio.OmisosNovedad200.Function/coverage.opencover.xml'

  - task: SonarQubeAnalyze@5
    displayName: Run Code Analysis
    inputs:
      jdkversion: 'JAVA_HOME_21_X64'

  - task: SonarQubePublish@5
    displayName: Publish Quality Gate Result
    inputs:
      pollingTimeoutSec: '500'

  - task: sonar-buildbreaker@8
    displayName: Break build on quality gate failure
    inputs:
      SonarQube: 'Sonar Qube 8.3-Fanaia Administradora'

  - task: PostBuildCleanup@3
    displayName: Clean Agent Directories
