2026-11-06T19:01:11.3333629Z ##[section]Starting: Ejecutar pruebas unitarias con cobertura
2026-11-06T19:01:11.3343513Z ==============================================================================
2026-11-06T19:01:11.3343619Z Task         : .NET Core
2026-11-06T19:01:11.3343684Z Description  : Build, test, package, or publish a dotnet application, or run a custom dotnet command
2026-11-06T19:01:11.3343777Z Version      : 2.281.1
2026-11-06T19:01:11.3343841Z Author       : Microsoft Corporation
2026-11-06T19:01:11.3343904Z Help         : https://docs.microsoft.com/azure/devops/pipelines/tasks/build/dotnet-core-cli
2026-11-06T19:01:11.3344032Z ==============================================================================
2026-11-06T19:01:12.0255747Z [command]C:\WINDOWS\system32\chcp.com 65001
2026-11-06T19:01:12.0644794Z Active code page: 65001
2026-11-06T19:01:12.0756957Z Info: .NET Core SDK/runtime 2.2 and 3.0 are now End of Life(EOL) and have been removed from all hosted agents. If you're using these SDK/runtimes on hosted agents, kindly upgrade to newer versions which are not EOL, or else use UseDotNet task to install the required version.
2026-11-06T19:01:12.0811538Z [command]"C:\Program Files\dotnet\dotnet.exe" test C:\AG\dev\d_4\_work\104\s\AEL.LogsBancarios.ActivarProceso.Function\AEL.LogsBancarios.ActivarProceso.Tests\ActivarProcesoLogsBancariosFunctionTests.cs --logger trx --results-directory C:\AG\dev\d_4\_work\_temp --configuration Release --no-*** "--collect:XPlat Code Coverage" -- DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.Format=opencover
2026-11-06T19:01:12.4801299Z C:\AG\dev\d_4\_work\104\s\AEL.LogsBancarios.ActivarProceso.Function\AEL.LogsBancarios.ActivarProceso.Tests\ActivarProcesoLogsBancariosFunctionTests.cs(1,1): error MSB4025: The project file could not be loaded. Data at the root level is invalid. Line 1, position 1.
2026-11-06T19:01:12.5154721Z 
2026-11-06T19:01:12.5303511Z ##[error]Error: The process 'C:\Program Files\dotnet\dotnet.exe' failed with exit code 1
2026-11-06T19:01:12.5315194Z ##[warning]No test result files were found.
2026-11-06T19:01:12.5317627Z ##[warning].NET 5 has some compatibility issues with older Nuget versions(<=5.7), so if you are using an older Nuget version(and not dotnet cli) to restore, then the dotnet cli commands (e.g. dotnet ***) which rely on such restored packages might fail. To mitigate such error, you can either: (1) - Use dotnet cli to restore, (2) - Use Nuget version 5.8 to restore, (3) - Use global.json using an older sdk version(<=3) to ***
2026-11-06T19:01:12.5319454Z Info: Azure Pipelines hosted agents have been updated and now contain .Net 5.x SDK/Runtime along with the older .Net Core version which are currently lts. Unless you have locked down a SDK version for your project(s), 5.x SDK might be picked up which might have breaking behavior as compared to previous versions. You can learn more about the breaking changes here: https://docs.microsoft.com/en-us/dotnet/core/tools/ and https://docs.microsoft.com/en-us/dotnet/core/compatibility/ . To learn about more such changes and troubleshoot, refer here: https://docs.microsoft.com/en-us/azure/devops/pipelines/tasks/***/dotnet-core-cli?view=azure-devops#troubleshooting
2026-11-06T19:01:12.5321344Z ##[error]Dotnet command failed with non-zero exit code on the following projects : [
  'C:\\AG\\dev\\d_4\\_work\\104\\s\\AEL.LogsBancarios.ActivarProceso.Function\\AEL.LogsBancarios.ActivarProceso.Tests\\ActivarProcesoLogsBancariosFunctionTests.cs'
]
2026-11-06T19:01:12.5490819Z ##[section]Finishing: Ejecutar pruebas unitarias con cobertura
