#Your build pipeline references an undefined variable named ‘buildconfiguration’. Create or edit the build pipeline for this YAML file, define the variable on the Variables tab. See https://go.microsoft.com/fwlink/?linkid=865972

steps:
- task: DotNetCoreCLI@2
  displayName: 'dotnet test'
  inputs:
    command: test
    projects: '$(build.sourcesDirectory)/AEL.Fanaia.DistribucionAportesPension.API/AEL.Fanaia.DAP.Test/AEL.Fanaia.DAP.Test.csproj'
    arguments: '--configuration $(buildconfiguration) --no-build /p:CollectCoverage=true /p:CoverletOutputFormat=opencover /p:CoverletOutput=$(Build.SourcesDirectory)/AEL.Fanaia.DistribucionAportesPension.API/AEL.Fanaia.DAP.Test/coverage.opencover.xml'
    testRunTitle: UnitTestProcesosSFTP

RUTA DEL TEST AEL.Interconexion.Test/AEL.Interconexion.Test.csproj

<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>

    <IsPackable>false</IsPackable>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="coverlet.collector" Version="10.0.1">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
    <PackageReference Include="coverlet.msbuild" Version="10.0.1">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="18.10.1" />
    <PackageReference Include="Moq" Version="4.21.0" />
    <PackageReference Include="System.Net.Http" Version="4.3.4" />
    <PackageReference Include="System.Text.RegularExpressions" Version="4.3.1" />
    <PackageReference Include="xunit" Version="2.9.3" />
    <PackageReference Include="xunit.runner.visualstudio" Version="4.0.0">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\AEL.Utils.DataAccess\AEL.Utils.DataAccess.csproj" />
    <ProjectReference Include="..\AEL.Utils.EstadosArchivos\AEL.Utils.EstadosArchivos.csproj" />
    <ProjectReference Include="..\AEL.Utils.Logger\AEL.Utils.Logger.csproj" />
    <ProjectReference Include="..\AEL.Utils.MsgProcess\AEL.Utils.MsgProcess.csproj" />
    <ProjectReference Include="..\AEL.Utils.Queue\AEL.Utils.Queue.csproj" />
    <ProjectReference Include="..\sftp\AEL.ProcesosSFTP.BLL\AEL.ProcesosSFTP.BLL.csproj" />
    <ProjectReference Include="..\succed\AEL.CifradoBanRep.BLL\AEL.CifradoBanRep.BLL.csproj" />
    <ProjectReference Include="..\succed\AEL.CifradoBanRep.BLL\AEL.CifradoBanRep.BLL.csproj" />

    
  </ItemGroup>

  <ItemGroup>
    <Using Include="Xunit" />
  </ItemGroup>

</Project>
