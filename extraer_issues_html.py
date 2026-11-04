
name: $(date:yyyyMMdd)$(rev:.r)
jobs:
- job: Phase_1
  displayName: Trabajo de agente 1
  pool:
    name: DEV
  steps:
  - checkout: self
    clean: true
  - task: CmdLine@1
    name: CmdLine_1
    displayName: Run C:\Tools\CredentialProvider\CredentialProvider.TeamBuild.exe
    enabled: False
    inputs:
      filename: C:\Tools\CredentialProvider\CredentialProvider.TeamBuild.exe
      arguments: -uri http://hiroshima01s:8080/tfs/Transversales/_packaging/ControlAcceso/nuget/v3/index.json -nonInteractive -verbosity detailed
  
  - task: NuGetAuthenticate@1
    inputs:
      nuGetServiceConnections: 'Feed_Transversales_Auditoria, Feed_Transversales_ControlAcceso, Feed_Transversales_Notificaciones, Feed_Transversales_Personas'

  - task: NuGetCommand@2
    inputs:
      command: 'restore'
      restoreSolution: 'Mareigua.Fanaia.Novedades/Mareigua.Fanaia.Novedades.sln'
      feedsToUse: 'config'
      nugetConfigPath: 'Nuget/nuget.config'

  - task: CmdLine@1
    name: CmdLine_3
    displayName: Run C:\Program Files (x86)\NuGet\Nuget.exe
    inputs:
      filename: C:\Program Files (x86)\NuGet\Nuget.exe
      arguments: update Mareigua.Fanaia.Novedades.sln -NonInteractive -ConfigFile "../Nuget/nuget.config" -FileConflictAction Overwrite
      workingFolder: Mareigua.Fanaia.Novedades

  - task: CmdLine@1
    name: CmdLine_4
    displayName: Copia de Run C:\Program Files (x86)\NuGet\Nuget.exe
    inputs:
      filename: C:\Program Files (x86)\NuGet\Nuget.exe
      arguments: update Mareigua.Fanaia.Novedades.sln -NonInteractive -ConfigFile "../Nuget/nuget.config" -FileConflictAction Overwrite -prerelease -source $(FeedsNugetUpdate)
      workingFolder: Mareigua.Fanaia.Novedades

  - task: SonarQubePrepare@7
    displayName: Prepare Analysis SonarQube
    inputs:
      SonarQube: 'Sonar-NovedadesRefactor'
      scannerMode: 'dotnet'
      projectKey: 'Mareigua.Fanaia.Novedades:Quality'
      projectName: 'Mareigua.Fanaia.Novedades:Quality'
      projectVersion: '$(Build.BuildNumber)_$(Build.SourceBranchName)'

  - task: MSBuild@1
    name: MSBuild_6
    displayName: Build solution Mareigua.Fanaia.Novedades/Mareigua.Fanaia.Novedades.sln
    inputs:
      solution: Mareigua.Fanaia.Novedades/Mareigua.Fanaia.Novedades.sln
      platform: $(BuildPlatform)
      configuration: $(BuildConfiguration)
      msbuildArguments: /p:DeployOnBuild=True /p:DeployDefaultTarget=WebPublish /p:WebPublishMethod=FileSystem /p:DeleteExistingFiles=True /p:publishUrl=$(build.artifactstagingdirectory)\Mareigua.Fanaia.Novedades.Servicio /p:ExcludeFoldersFromDeployment="App_Code" /p:PrecompileBeforePublish=True /p:WDPMergeOption=CreateSeparateAssembly /p:PrecompileBeforePublish=true  

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
      SonarQube: Sonar-NovedadesRefactor

  - task: PostBuildCleanup@3
    displayName: Clean Agent Directories
...
