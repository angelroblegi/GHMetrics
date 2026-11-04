
name: $(date:yyyyMMdd)$(rev:.r)
jobs:
- job: Phase_1
  displayName: Trabajo de agente 1
  pool:
    name: DEV
  steps:
  - checkout: self
    clean: true
  - task: NuGetAuthenticate@1
    displayName: Autenticar
    inputs:
      nuGetServiceConnections: 'Feed_Transversales_Auditoria, Feed_Transversales_ControlAcceso, Feed_Transversales_Notificaciones, Feed_Transversales_Personas'
  - task: CmdLine@1
    name: CmdLine_1
    displayName: Run C:\Tools\CredentialProvider\CredentialProvider.TeamBuild.exe
    enabled: False
    inputs:
      filename: C:\Tools\CredentialProvider\CredentialProvider.TeamBuild.exe
      arguments: -uri https://pkgs.dev.azure.com/AEL-Transversales/_packaging/ControlAcceso/nuget/v3/index.json -nonInteractive -verbosity detailed
  - task: NuGetInstaller@0
    name: NuGetInstaller_2
    enabled: False
    displayName: NuGet restore Mareigua.Fanaia.Novedades.Refactor.sln
    inputs:
      solution: Mareigua.Fanaia.Novedades.Refactor/Mareigua.Fanaia.Novedades.Refactor.sln
      nugetConfigPath: Nuget/nuget.config
      verbosity: Detailed
      nuGetVersion: 4.0.0.2283
      nuGetPath: C:\Program Files (x86)\NuGet\Nuget.exe
  - task: NuGetCommand@2
    inputs:
      command: 'restore'
      restoreSolution: 'Mareigua.Fanaia.Novedades.Refactor/Mareigua.Fanaia.Novedades.Refactor.sln'
      feedsToUse: 'config'
      nugetConfigPath: '$(build.sourcesdirectory)/Nuget/nuget.config'
  - task: CmdLine@1
    name: CmdLine_3
    displayName: Run C:\Program Files (x86)\NuGet\Nuget.exe
    inputs:
      filename: C:\Program Files (x86)\NuGet\Nuget.exe
      arguments: update Mareigua.Fanaia.Novedades.Refactor.sln -NonInteractive -ConfigFile "../Nuget/nuget.config" -FileConflictAction Overwrite
      workingFolder: Mareigua.Fanaia.Novedades.Refactor
  - task: CmdLine@1
    name: CmdLine_4
    displayName: Copia de Run C:\Program Files (x86)\NuGet\Nuget.exe
    inputs:
      filename: C:\Program Files (x86)\NuGet\Nuget.exe
      arguments: update Mareigua.Fanaia.Novedades.Refactor.sln -NonInteractive -ConfigFile "../Nuget/nuget.config" -FileConflictAction Overwrite -prerelease -source $(FeedPreRelease)
      workingFolder: Mareigua.Fanaia.Novedades.Refactor
  
  - task: SonarQubePrepare@7
    inputs:
      SonarQube: 'Sonar-NovedadesRefactor'
      scannerMode: 'dotnet'
      projectKey: 'Mareigua.Fanaia.Novedades.Refactor:Quality'
      projectName: 'Mareigua.Fanaia.Novedades.Refactor:Quality'
      projectVersion: '$(Build.BuildNumber)_$(Build.SourceBranchName)'
      extraProperties: |
        sonar.cs.opencover.reportsPaths=$(Build.SourcesDirectory)/Mareigua.Fanaia.Novedades.Refactor/Mareigua.Fanaia.Novedades.Refactor/coverage.opencover.xml
        sonar.scm.provider=git
  - task: MSBuild@1
    name: MSBuild_6
    displayName: Build solution Mareigua.Fanaia.Novedades.Refactor/Mareigua.Fanaia.Novedades.Refactor.sln
    inputs:
      solution: Mareigua.Fanaia.Novedades.Refactor/Mareigua.Fanaia.Novedades.Refactor.sln
      platform: $(BuildPlatform)
      configuration: $(BuildConfiguration)
      msbuildArguments: /p:DeployOnBuild=True /p:DeployDefaultTarget=WebPublish /p:WebPublishMethod=FileSystem /p:DeleteExistingFiles=True /p:publishUrl=$(build.artifactstagingdirectory)\Mareigua.Fanaia.Novedades.Refactor.Servicio\Publish\ /p:ExcludeFoldersFromDeployment="App_Code" /p:PrecompileBeforePublish=True /p:WDPMergeOption=CreateSeparateAssembly /p:PrecompileBeforePublish=true    

  - task: MSBuild@1
    name: MSBuild_5
    displayName: Build solution Test
    inputs:
        solution: $(build.sourcesdirectory)/Mareigua.Fanaia.Novedades.Refactor/Mareigua.Fanaia.Novedades.RefactorTest/Mareigua.Fanaia.Novedades.RefactorTest.csproj
        msbuildVersion: 15.0
        msbuildArchitecture: x64
        configuration: $(buildConfiguration)      

  - script: dir $(Build.SourcesDirectory)\Mareigua.Fanaia.Novedades.Refactor\Mareigua.Fanaia.Novedades.RefactorTest
  - script: dir $(Build.SourcesDirectory)\Mareigua.Fanaia.Novedades.Refactor\Mareigua.Fanaia.Novedades.RefactorTest\bin
  - script: dir $(Build.SourcesDirectory)\Mareigua.Fanaia.Novedades.Refactor\Mareigua.Fanaia.Novedades.RefactorTest\bin\release
  
  - task: CmdLine@2
    displayName: 'Ejecutar OpenCover y Tests'
    inputs:
      script: |
          echo "Creando directorio de salida si no existe..."
          if not exist "$(Build.SourcesDirectory)\Mareigua.Fanaia.Novedades.Refactor\Mareigua.Fanaia.Novedades.Refactor" mkdir "$(Build.SourcesDirectory)\Mareigua.Fanaia.Novedades.Refactor\Mareigua.Fanaia.Novedades.Refactor"

          echo "Ejecutando OpenCover..."
          OpenCover.Console.exe ^
            -target:"C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\Common7\IDE\CommonExtensions\Microsoft\TestWindow\vstest.console.exe" ^
            -targetargs:"$(Build.SourcesDirectory)\Mareigua.Fanaia.Novedades.Refactor\Mareigua.Fanaia.Novedades.RefactorTest\bin\release\Mareigua.Fanaia.Novedades.RefactorTest.dll" ^
            -register:path64 ^
            -filter:"+[Mareigua*]* -[*Test]*" ^
            -mergebyhash ^
            -output:"$(Build.SourcesDirectory)\Mareigua.Fanaia.Novedades.Refactor\Mareigua.Fanaia.Novedades.Refactor\coverage.opencover.xml"
          
          echo "Verificando existencia del archivo..."
          dir "$(Build.SourcesDirectory)\Mareigua.Fanaia.Novedades.Refactor\Mareigua.Fanaia.Novedades.Refactor\coverage.opencover.xml"   
  - task: SonarQubeAnalyze@7
    inputs:
      jdkversion: 'JAVA_HOME_17_X64'
  - task: SonarQubePublish@7
    inputs:
      pollingTimeoutSec: '500'
  - task: sonar-buildbreaker@8
    displayName: Break build on quality gate failure
    inputs:
      SonarQube: Sonar-NovedadesRefactor
  - task: PostBuildCleanup@3
    displayName: Clean Agent Directories
...

<Project Sdk="Microsoft.NET.Sdk">


  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
  </PropertyGroup>


  <ItemGroup>
    <PackageReference Include="coverlet.collector" Version="6.0.4" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.14.1" />
    <PackageReference Include="Moq" Version="4.21.0" />
    <PackageReference Include="xunit" Version="2.9.3" />
    <PackageReference Include="xunit.runner.visualstudio" Version="3.1.4" />
  </ItemGroup>


  <ItemGroup>
    <ProjectReference Include="..\AEL.Fanaia.NovedadVSP.API\AEL.Fanaia.NovedadVSP.API.csproj" />
  </ItemGroup>


  <ItemGroup>
    <Using Include="Xunit" />
  </ItemGroup>


</Project>

AEL.Fanaia.NovedadVSP.API/AEL.Fanaia.NovedadVSP.API.Tests/AEL.Fanaia.NovedadVSP.API.Tests.csproj

    
