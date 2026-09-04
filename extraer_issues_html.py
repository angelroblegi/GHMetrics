name: $(date:yyyyMMdd)$(rev:.r)
jobs:
- job: Phase_1
  displayName: Agent job 1
  pool:
    name: DEV
  steps:
  - checkout: self
    clean: true

  - task: NuGetAuthenticate@1
    inputs:
      nuGetServiceConnections: 'Feed_Transversales_Auditoria, Feed_Transversales_ControlAcceso, Feed_Transversales_PasarelaPagos, Feed_Transversales_Personas, Feed_Transversales_ProdNotificaciones, Feed_Transversales_TerminosYCondiciones'

  - task: NuGetCommand@2
    name: NuGetInstaller_1
    displayName: NuGet restore $(build.sourcesDirectory)\Mareigua\Fanaia\Pagos\AplicacionWeb\Mareigua.Fanaia.Pagos.AplicacionWeb\Mareigua.Fanaia.Pagos.AplicacionWeb.sln
    inputs:
      command: 'restore'
      restoreSolution: '$(build.sourcesDirectory)\Mareigua\Fanaia\Pagos\AplicacionWeb\Mareigua.Fanaia.Pagos.AplicacionWeb\Mareigua.Fanaia.Pagos.AplicacionWeb.sln'
      feedsToUse: 'config'
      nugetConfigPath: '$(build.sourcesdirectory)\Nuget\nuget.config'

  - task: CmdLine@1
    displayName: Update Nuget release
    inputs:
      filename: C:\Program Files (x86)\NuGet\Nuget.exe
      arguments: update Mareigua.Fanaia.Pagos.AplicacionWeb.sln -NonInteractive -ConfigFile $(build.sourcesDirectory)\Nuget\nuget.config
      workingFolder: $(build.sourcesDirectory)/Mareigua/Fanaia/Pagos/AplicacionWeb/Mareigua.Fanaia.Pagos.AplicacionWeb/

  - task: CmdLine@1
    displayName: Update nuget prerelease
    inputs:
      filename: C:\Program Files (x86)\NuGet\Nuget.exe
      arguments: update -DependencyVersion Ignore Mareigua.Fanaia.Pagos.AplicacionWeb.sln -NonInteractive -ConfigFile $(build.sourcesDirectory)\Nuget\nuget.config -source $(FeedsNugetUpdate) -prerelease
      workingFolder: $(build.sourcesDirectory)/Mareigua/Fanaia/Pagos/AplicacionWeb/Mareigua.Fanaia.Pagos.AplicacionWeb/

  - task: SonarQubePrepare@8
    displayName: Prepare analysis on SonarQube
    inputs:
      SonarQube: 'Sonar Qube 8.3'
      scannerMode: 'dotnet'
      projectKey: 'Mareigua.Fanaia.Pagos.AplicacionWeb:Quality'
      projectName: 'Mareigua.Fanaia.Pagos.AplicacionWeb:Quality'
      projectVersion: '$(Build.BuildNumber)_$(Build.SourceBranchName)'
      extraProperties: |
        sonar.projectBaseDir=$(Build.SourcesDirectory)/Mareigua/Fanaia/Pagos/AplicacionWeb/Mareigua.Fanaia.Pagos.AplicacionWeb
        sonar.exclusions=Scripts/jquery-3.1.1.slim.js,**/Mareigua.Fanaia.Pagos.AplicacionWeb/Scripts/jquery-3.1.1.js,**/Mareigua.Fanaia.Pagos.AplicacionWeb/Scripts/jquery-3.1.1.slim.js

  - task: VSBuild@1
    name: VSBuild_3
    displayName: Build solution $(build.sourcesDirectory)/Mareigua/Fanaia/Pagos/AplicacionWeb/Mareigua.Fanaia.Pagos.AplicacionWeb/Mareigua.Fanaia.Pagos.AplicacionWeb.sln
    inputs:
      solution: '$(build.sourcesDirectory)/Mareigua/Fanaia/Pagos/AplicacionWeb/Mareigua.Fanaia.Pagos.AplicacionWeb/Mareigua.Fanaia.Pagos.AplicacionWeb.sln'
      msbuildArgs: '/p:DeployOnBuild=True /p:DeployDefaultTarget=WebPublish /p:WebPublishMethod=FileSystem /p:DeleteExistingFiles=True /p:publishUrl=$(build.artifactstagingdirectory)\Mareigua.Fanaia.Pagos.AplicacionWeb /p:ExcludeFoldersFromDeployment="App_Code"'
      platform: '$(BuildPlatform)'
      configuration: '$(BuildConfiguration)'
      msbuildArchitecture: 'x64'

  - task: SonarQubeAnalyze@8
    displayName: Run Code Analysis
    inputs:
      jdkversion: 'JAVA_HOME_21_X64'

  - task: SonarQubePublish@8
    displayName: Publish Quality Gate Result
    inputs:
      pollingTimeoutSec: '500'

  - task: sonar-buildbreaker@8
    displayName: Break build on quality gate failure
    inputs:
      SonarQube: 'Sonar Qube 8.3'

  - task: BatchScript@1
    name: BatchScript_5
    displayName: Limpiar Paquete
    inputs:
      filename: $(build.sourcesdirectory)/Applications/WinApplications/LimpiarPaquete.BAT
      modifyEnvironment: false
      workingFolder: $(build.artifactstagingdirectory)

  - task: PostBuildCleanup@3
    displayName: Clean Agent Directories
...
