Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 17
VisualStudioVersion = 17.14.36109.1
MinimumVisualStudioVersion = 10.0.40219.1
Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "AEL.Administradora.CargueDatosBDReferencia.Domain", "AEL.Administradora.CargueDatosBDReferencia.Domain\AEL.Administradora.CargueDatosBDReferencia.Domain.csproj", "{B31A4FFF-F296-4CF2-8256-9993694F06C5}"
EndProject
Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "AEL.Administradora.CargueDatosBDReferencia.Infrastruture", "AEL.Administradora.CargueDatosBDReferencia.Infrastruture\AEL.Administradora.CargueDatosBDReferencia.Infrastruture.csproj", "{0EBB6216-C0CD-4025-B15A-65F96C598BF9}"
EndProject
Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "AEL.Administradora.CargueDatosBDReferencia.Application", "AEL.Administradora.CargueDatosBDReferencia.Application\AEL.Administradora.CargueDatosBDReferencia.Application.csproj", "{34C1FDC5-631B-4B4B-AA7A-C08436CF9A8C}"
EndProject
Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "AEL.Administradora.CargueDatosBDReferencia.Test", "AEL.Administradora.CargueDatosBDReferencia.Test\AEL.Administradora.CargueDatosBDReferencia.Test.csproj", "{99207A88-D152-419B-A31E-3913F5475D7E}"
EndProject
Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "AEL.Administradora.CargueDatosBDReferencia.Funcion", "AEL.Administradora.CargueDatosBDReferencia.Funcion\AEL.Administradora.CargueDatosBDReferencia.Funcion.csproj", "{768425CC-340C-C31C-070D-17CF0FAA7780}"
EndProject
Global
	GlobalSection(SolutionConfigurationPlatforms) = preSolution
		Debug|Any CPU = Debug|Any CPU
		Release|Any CPU = Release|Any CPU
	EndGlobalSection
	GlobalSection(ProjectConfigurationPlatforms) = postSolution
		{B31A4FFF-F296-4CF2-8256-9993694F06C5}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
		{B31A4FFF-F296-4CF2-8256-9993694F06C5}.Debug|Any CPU.Build.0 = Debug|Any CPU
		{B31A4FFF-F296-4CF2-8256-9993694F06C5}.Release|Any CPU.ActiveCfg = Release|Any CPU
		{B31A4FFF-F296-4CF2-8256-9993694F06C5}.Release|Any CPU.Build.0 = Release|Any CPU
		{0EBB6216-C0CD-4025-B15A-65F96C598BF9}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
		{0EBB6216-C0CD-4025-B15A-65F96C598BF9}.Debug|Any CPU.Build.0 = Debug|Any CPU
		{0EBB6216-C0CD-4025-B15A-65F96C598BF9}.Release|Any CPU.ActiveCfg = Release|Any CPU
		{0EBB6216-C0CD-4025-B15A-65F96C598BF9}.Release|Any CPU.Build.0 = Release|Any CPU
		{34C1FDC5-631B-4B4B-AA7A-C08436CF9A8C}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
		{34C1FDC5-631B-4B4B-AA7A-C08436CF9A8C}.Debug|Any CPU.Build.0 = Debug|Any CPU
		{34C1FDC5-631B-4B4B-AA7A-C08436CF9A8C}.Release|Any CPU.ActiveCfg = Release|Any CPU
		{34C1FDC5-631B-4B4B-AA7A-C08436CF9A8C}.Release|Any CPU.Build.0 = Release|Any CPU
		{99207A88-D152-419B-A31E-3913F5475D7E}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
		{99207A88-D152-419B-A31E-3913F5475D7E}.Debug|Any CPU.Build.0 = Debug|Any CPU
		{99207A88-D152-419B-A31E-3913F5475D7E}.Release|Any CPU.ActiveCfg = Release|Any CPU
		{99207A88-D152-419B-A31E-3913F5475D7E}.Release|Any CPU.Build.0 = Release|Any CPU
		{768425CC-340C-C31C-070D-17CF0FAA7780}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
		{768425CC-340C-C31C-070D-17CF0FAA7780}.Debug|Any CPU.Build.0 = Debug|Any CPU
		{768425CC-340C-C31C-070D-17CF0FAA7780}.Release|Any CPU.ActiveCfg = Release|Any CPU
		{768425CC-340C-C31C-070D-17CF0FAA7780}.Release|Any CPU.Build.0 = Release|Any CPU
	EndGlobalSection
	GlobalSection(SolutionProperties) = preSolution
		HideSolutionNode = FALSE
	EndGlobalSection
	GlobalSection(ExtensibilityGlobals) = postSolution
		SolutionGuid = {242D2574-4DB3-4FAE-AEC5-A7FCDD93C8F1}
	EndGlobalSection
EndGlobal

AEL.Administradora.CargueDatosBDReferencia/AEL.Administradora.CargueDatosBDReferencia.sln

CS PROJ TEST
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>

    <IsPackable>false</IsPackable>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Azure.Core" Version="1.55.0" />
    <PackageReference Include="Azure.Storage.Queues" Version="12.27.1" />
    <PackageReference Include="coverlet.collector" Version="6.0.0" />
    <PackageReference Include="FluentAssertions" Version="8.5.0" />
    <PackageReference Include="MediatR" Version="12.5.0" />
    <PackageReference Include="Microsoft.Extensions.Logging.Abstractions" Version="10.0.10" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageReference Include="Moq" Version="4.20.72" />
    <PackageReference Include="xunit" Version="2.5.3" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.3" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\AEL.Administradora.CargueDatosBDReferencia.Application\AEL.Administradora.CargueDatosBDReferencia.Application.csproj" />
    <ProjectReference Include="..\AEL.Administradora.CargueDatosBDReferencia.Funcion\AEL.Administradora.CargueDatosBDReferencia.Funcion.csproj" />
  </ItemGroup>

  <ItemGroup>
    <Using Include="Xunit" />
  </ItemGroup>

</Project>
AEL.Administradora.CargueDatosBDReferencia/AEL.Administradora.CargueDatosBDReferencia.Test/AEL.Administradora.CargueDatosBDReferencia.Test.csproj


EJEMPLO DE OTRO PIPELINE DEL MISMO REPO
name: $(date:yyyyMMdd)$(rev:.r)
variables:
  solution: 'AEL.Administradora.Cifrado.Function/AEL.Administradora.Cifrado.Function.sln'
  projectPath: '$(Build.SourcesDirectory)/AEL.Administradora.Cifrado.Function'
  sonarProject: 'AEL.Administradora.Cifrado.Function:Quality'
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
      projects: '$(solution)'
      feedsToUse: 'select'
 
  - task: SonarQubePrepare@5
    displayName: Prepare analysis on SonarQube
    inputs:
      SonarQube: c920b15f-1de4-45cf-8de8-00186bd2439a
      scannerMode: 'CLI'
      configMode: 'manual'
      cliProjectKey: '$(sonarProject)'
      cliProjectName: '$(sonarProject)'
      cliProjectVersion: '$(Build.BuildNumber)_$(Build.SourceBranchName)'
      cliSources: '$(projectPath)/'
      extraProperties: |
        # Additional properties that will be passed to the scanner, 
        # Put one key=value per line, example:
        sonar.coverage.exclusions=AEL.Administradora.Cifrado.Function/AEL.Administradora.Cifrado.Function/Program.cs,AEL.Administradora.Cifrado.Function/AEL.Administradora.Cifrado.Function/Middlewares/ExceptionHandlingMiddleware.cs,AEL.Administradora.Cifrado.Function/AEL.Administradora.Cifrado.Function/Helpers/Wrappers/*.cs
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
      projects: '$(projectPath)/AEL.Administradora.Cifrado.Function/AEL.Administradora.Cifrado.Function.csproj'
      arguments: '--configuration Release'
      
  - task: DotNetCoreCLI@2
    displayName: 'Ejecutar pruebas unitarias con cobertura'
    enabled: True
    inputs:
      command: 'test'
      projects: '$(projectPath)/AEL.Administradora.Cifrado.Tests/AEL.Administradora.Cifrado.Tests.csproj'
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

