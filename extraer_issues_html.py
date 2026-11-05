name: $(date:yyyyMMdd)$(rev:.r)
variables:
  solution: 'AEL.BDReferencia.DoubleMetaphone.Function/AEL.BDReferencia.DoubleMetaphone.Function.sln'
  projectPath: '$(Build.SourcesDirectory)/AEL.BDReferencia.DoubleMetaphone.Function'
  sonarProject: 'AEL.BDReferencia.DoubleMetaphone.Function:Quality'
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
      feedsToUse: 'config'
      nugetConfigPath: '$(build.sourcesDirectory)/AEL.BDReferencia.DoubleMetaphone.Function/nuget.config'
 
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
        sonar.coverage.exclusions=AEL.BDReferencia.DoubleMetaphone.Function/AEL.BDReferencia.DoubleMetaphone.Function/Program.cs
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
      projects: '$(projectPath)/AEL.BDReferencia.DoubleMetaphone.Function/AEL.BDReferencia.DoubleMetaphone.Function.csproj'
      arguments: '--configuration Release'
      
  - task: DotNetCoreCLI@2
    displayName: 'Ejecutar pruebas unitarias con cobertura'
    enabled: True
    inputs:
      command: 'test'
      projects: '$(projectPath)/AEL.BDReferencia.DoubleMetaphone.Tests/AEL.BDReferencia.DoubleMetaphone.Tests.csproj'
      arguments: '--configuration Release /p:CollectCoverage=true /p:CoverletOutputFormat=opencover /p:CoverletOutput=$(projectPath)/coverage.opencover.xml'
  
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


[More Information](https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarqube-extension-for-azure-devops/)
2026-11-05T15:51:27.1663555Z ==============================================================================
2026-11-05T15:51:27.7880292Z ##[warning]This task is deprecated. Please upgrade to the latest version. For more information, refer to https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarqube-extension-for-azure-devops/
2026-11-05T15:51:27.7886239Z ##[warning]This task was configured to use Java 11, but the SonarQube server v2025.1.0 does not support it. Ignoring the configuration and using JAVA_HOME instead. Specify jdkversion in your task definition to use Java 17 to remove this warning.
2026-11-05T15:51:27.7916742Z [command]C:\AG\dev\d_5\_work\_tasks\SonarQubePrepare_15b84ca1-b62f-4a2a-a403-89b77a063157\5.19.2\classic-sonar-scanner-ms***\SonarScanner.MSBuild.exe end
2026-11-05T15:51:28.0607865Z SonarScanner for MSBuild 5.15.1
2026-11-05T15:51:28.0609767Z Using the .NET Framework version of the Scanner for MSBuild
2026-11-05T15:51:28.1868794Z Post-processing started.
2026-11-05T15:51:28.5166145Z Calling the TFS Processor executable...
2026-11-05T15:51:28.9239386Z Attempting to locate the CodeCoverage.exe tool...
2026-11-05T15:51:28.9290753Z Attempting to locate the CodeCoverage.exe tool using setup configuration...
2026-11-05T15:51:29.0041436Z Attempting to locate the CodeCoverage.exe tool using registry...
2026-11-05T15:51:29.0109946Z WARNING: Failed to find the code coverage command line tool. Possible cause: Visual Studio is not installed, or the installed version does not support code coverage.
2026-11-05T15:51:29.0348762Z The TFS Processor has finished
2026-11-05T15:51:29.0421599Z Calling the SonarScanner CLI...
2026-11-05T15:51:29.3912888Z 
2026-11-05T15:51:29.3922147Z ERROR: JAVA_HOME exists but does not point to a valid Java home
2026-11-05T15:51:29.3928814Z        folder. No "\bin\java.exe" file can be found there.
2026-11-05T15:51:29.3994983Z 
2026-11-05T15:51:29.4303064Z ##[error]The SonarScanner did not complete successfully
2026-11-05T15:51:29.4304226Z The SonarScanner did not complete successfully
2026-11-05T15:51:29.4304940Z ##[error]10:51:29.416  Post-processing failed. Exit code: 1
2026-11-05T15:51:29.4305426Z 10:51:29.416  Post-processing failed. Exit code: 1
2026-11-05T15:51:29.4467589Z ##[warning]LIB_ResourceFile does not exist
2026-11-05T15:51:29.4469831Z ##[warning]Resource file haven't been set, can't find loc string for key: LIB_ProcessExitCode
2026-11-05T15:51:29.4471503Z ##[warning]Error while executing SonarQube:Analyze task: LIB_ProcessExitCode C:\AG\dev\d_5\_work\_tasks\SonarQubePrepare_15b84ca1-b62f-4a2a-a403-89b77a063157\5.19.2\classic-sonar-scanner-ms***\SonarScanner.MSBuild.exe 1
2026-11-05T15:51:29.4473561Z ##[error]LIB_ProcessExitCode C:\AG\dev\d_5\_work\_tasks\SonarQubePrepare_15b84ca1-b62f-4a2a-a403-89b77a063157\5.19.2\classic-sonar-scanner-ms***\SonarScanner.MSBuild.exe 1
2026-11-05T15:51:29.4618090Z ##[section]Finishing: Run Code Analysis
