2026-11-06T15:48:35.4056127Z ##[section]Starting: Ejecutar pruebas unitarias con cobertura
2026-11-06T15:48:35.4070802Z ==============================================================================
2026-11-06T15:48:35.4070960Z Task         : .NET Core
2026-11-06T15:48:35.4071050Z Description  : Build, test, package, or publish a dotnet application, or run a custom dotnet command
2026-11-06T15:48:35.4071179Z Version      : 2.281.1
2026-11-06T15:48:35.4071265Z Author       : Microsoft Corporation
2026-11-06T15:48:35.4071352Z Help         : https://docs.microsoft.com/azure/devops/pipelines/tasks/build/dotnet-core-cli
2026-11-06T15:48:35.4071473Z ==============================================================================
2026-11-06T15:48:36.2848206Z [command]C:\WINDOWS\system32\chcp.com 65001
2026-11-06T15:48:36.3340117Z Active code page: 65001
2026-11-06T15:48:36.3492895Z Info: .NET Core SDK/runtime 2.2 and 3.0 are now End of Life(EOL) and have been removed from all hosted agents. If you're using these SDK/runtimes on hosted agents, kindly upgrade to newer versions which are not EOL, or else use UseDotNet task to install the required version.
2026-11-06T15:48:36.3564668Z [command]"C:\Program Files\dotnet\dotnet.exe" test C:\AG\dev\d_6\_work\10\s\AEL.Administradora.CargueDatosBDReferencia\AEL.Administradora.CargueDatosBDReferencia.Test\AEL.Administradora.CargueDatosBDReferencia.Test.csproj --logger trx --results-directory C:\AG\dev\d_6\_work\_temp --configuration Release --no-build "--collect:XPlat Code Coverage" --results-directory C:\AG\dev\d_6\_work\_temp/TestResults -- DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.Format=opencover
2026-11-06T15:48:36.6466434Z 
2026-11-06T15:48:36.6471275Z Option '--results-directory' expects a single argument but 2 were provided.
2026-11-06T15:48:36.6471434Z 
2026-11-06T15:48:36.6480330Z Description:
2026-11-06T15:48:36.6480694Z   .NET Test Command for VSTest. To use Microsoft.Testing.Platform, opt-in to the Microsoft.Testing.Platform-based command via global.json. For more information, see https://aka.ms/dotnet-test.
2026-11-06T15:48:36.6480901Z 
2026-11-06T15:48:36.6491716Z Usage:
2026-11-06T15:48:36.6491963Z   dotnet test [options] [[--] <additional arguments>...]]
2026-11-06T15:48:36.6492073Z 
2026-11-06T15:48:36.6665439Z Options:
2026-11-06T15:48:36.6727837Z   -s, --settings <SETTINGS_FILE>       The settings file to use when running tests.
2026-11-06T15:48:36.6728296Z   -t, --list-tests                     List the discovered tests instead of running the tests. [default: False]
2026-11-06T15:48:36.6728594Z   -e, --environment <NAME="VALUE">     Sets the value of an environment variable. 
2026-11-06T15:48:36.6728866Z                                        Creates the variable if it does not exist, overrides if it does. 
2026-11-06T15:48:36.6729111Z                                        This will force the tests to be run in an isolated process. 
2026-11-06T15:48:36.6729334Z                                        This argument can be specified multiple times to provide multiple variables.
2026-11-06T15:48:36.6729523Z   
2026-11-06T15:48:36.6729704Z                                        Examples:
2026-11-06T15:48:36.6729896Z                                        -e VARIABLE=abc
2026-11-06T15:48:36.6730892Z                                        -e VARIABLE="value with spaces"
2026-11-06T15:48:36.6731157Z                                        -e VARIABLE="value;seperated with;semicolons"
2026-11-06T15:48:36.6731413Z                                        -e VAR1=abc -e VAR2=def -e VAR3=ghi
2026-11-06T15:48:36.6731646Z   --filter <EXPRESSION>                Run tests that match the given expression.
2026-11-06T15:48:36.6732149Z                                                                                Examples:
2026-11-06T15:48:36.6732340Z                                                                                Run tests with priority set to 1: --filter "Priority = 1"
2026-11-06T15:48:36.6732592Z                                                                                Run a test with the specified full name: --filter "FullyQualifiedName=Namespace.ClassName.MethodName"
2026-11-06T15:48:36.6734072Z                                                                                Run tests that contain the specified name: --filter "FullyQualifiedName~Namespace.Class"
2026-11-06T15:48:36.6734322Z                                                                                See https://aka.ms/vstest-filtering for more information on filtering support.
2026-11-06T15:48:36.6734566Z   --test-adapter-path <ADAPTER_PATH>   The path to the custom adapters to use for the test run.
2026-11-06T15:48:36.6734803Z   -l, --logger <LOGGER>                The logger to use for test results.
2026-11-06T15:48:36.6734992Z                                                                                Examples:
2026-11-06T15:48:36.6735178Z                                                                                Log in trx format using a unique file name: --logger trx
2026-11-06T15:48:36.6735423Z                                                                                Log in trx format using the specified file name: --logger "trx;LogFileName=<TestResults.trx>"
2026-11-06T15:48:36.6735676Z                                                                                See https://aka.ms/vstest-report for more information on logger arguments.
2026-11-06T15:48:36.6735902Z   -o, --output <OUTPUT_DIR>            The output directory to place built artifacts in.
2026-11-06T15:48:36.6736182Z   --artifacts-path <ARTIFACTS_DIR>     The artifacts path. All output from the project, including build, publish, and pack output, will go in subfolders under the specified path.
2026-11-06T15:48:36.6736457Z   -d, --diag <LOG_FILE>                Enable verbose logging to the specified file.
2026-11-06T15:48:36.6736689Z   --no-build                           Do not build the project before testing. Implies --no-restore. [default: False]
2026-11-06T15:48:36.6736941Z   --results-directory <RESULTS_DIR>    The directory where the test results will be placed.
2026-11-06T15:48:36.6737166Z                                        The specified directory will be created if it does not exist.
2026-11-06T15:48:36.6737399Z   --collect <DATA_COLLECTOR_NAME>      The friendly name of the data collector to use for the test run.
2026-11-06T15:48:36.6737620Z                                                                                More info here: https://aka.ms/vstest-collect
2026-11-06T15:48:36.6737900Z   --blame                              Runs the tests in blame mode. This option is helpful in isolating problematic tests that cause the test host to crash or hang, but it does not create a memory dump by default.
2026-11-06T15:48:36.6738150Z   
2026-11-06T15:48:36.6738458Z                                        When a crash is detected, it creates an sequence file in TestResults/guid/guid_Sequence.xml that captures the order of tests that were run before the crash.
2026-11-06T15:48:36.6738683Z   
2026-11-06T15:48:36.6738882Z                                        Based on the additional settings, hang dump or crash dump can also be collected.
2026-11-06T15:48:36.6739064Z   
2026-11-06T15:48:36.6739212Z                                        Example:
2026-11-06T15:48:36.6739441Z                                          Timeout the test run when test takes more than the default timeout of 1 hour, and collect crash dump when the test host exits unexpectedly.
2026-11-06T15:48:36.6739684Z                                          (Crash dumps require additional setup, see below.)
2026-11-06T15:48:36.6739979Z                                          dotnet test --blame-hang --blame-crash
2026-11-06T15:48:36.6740153Z                                        Example:
2026-11-06T15:48:36.6740351Z                                          Timeout the test run when a test takes more than 20 minutes and collect hang dump.
2026-11-06T15:48:36.6740558Z                                          dotnet test --blame-hang-timeout 20min
2026-11-06T15:48:36.6741077Z                                         [default: False]
2026-11-06T15:48:36.6741340Z   --blame-crash                        Runs the tests in blame mode and collects a crash dump when the test host exits unexpectedly. This option depends on the version of .NET used, the type of error, and the operating system.
2026-11-06T15:48:36.6741596Z   
2026-11-06T15:48:36.6741900Z                                        For exceptions in managed code, a dump will be automatically collected on .NET 5.0 and later versions. It will generate a dump for testhost or any child process that also ran on .NET 5.0 and crashed. Crashes in native code will not generate a dump. This option works on Windows, macOS, and Linux.
2026-11-06T15:48:36.6742207Z   
2026-11-06T15:48:36.6742507Z                                        Crash dumps in native code, or when targetting .NET Framework, or .NET Core 3.1 and earlier versions, can only be collected on Windows, by using Procdump. A directory that contains procdump.exe and procdump64.exe must be in the PATH or PROCDUMP_PATH environment variable.
2026-11-06T15:48:36.6742791Z   
2026-11-06T15:48:36.6742981Z                                        The tools can be downloaded here: https://docs.microsoft.com/sysinternals/downloads/procdump
2026-11-06T15:48:36.6743166Z   
2026-11-06T15:48:36.6743411Z                                        To collect a crash dump from a native application running on .NET 5.0 or later, the usage of Procdump can be forced by setting the VSTEST_DUMP_FORCEPROCDUMP environment variable to 1.
2026-11-06T15:48:36.6743652Z   
2026-11-06T15:48:36.6743806Z                                        Implies --blame. [default: False]
2026-11-06T15:48:36.6744041Z   --blame-crash-dump-type <DUMP_TYPE>  The type of crash dump to be collected. Supported values are full (default) and mini. Implies --blame-crash.
2026-11-06T15:48:36.6744330Z   --blame-crash-collect-always         Enables collecting crash dump on expected as well as unexpected testhost exit. [default: False]
2026-11-06T15:48:36.6744607Z   --blame-hang                         Run the tests in blame mode and enables collecting hang dump when test exceeds the given timeout. [default: False]
2026-11-06T15:48:36.6744948Z   --blame-hang-dump-type <DUMP_TYPE>   The type of crash dump to be collected. The supported values are full (default), mini, and none. When 'none' is used then test host is terminated on timeout, but no dump is collected. Implies --blame-hang.
2026-11-06T15:48:36.6745292Z   --blame-hang-timeout <TIMESPAN>      Per-test timeout, after which hang dump is triggered and the testhost process is terminated. Default is 1h.
2026-11-06T15:48:36.6745596Z                                        The timeout value is specified in the following format: 1.5h / 90m / 5400s / 5400000ms. When no unit is used (e.g. 5400000), the value is assumed to be in milliseconds.
2026-11-06T15:48:36.6745951Z                                        When used together with data driven tests, the timeout behavior depends on the test adapter used. For xUnit, NUnit and MSTest 2.2.4+ the timeout is renewed after every test case,
2026-11-06T15:48:36.6746222Z                                        For MSTest before 2.2.4, the timeout is used for all testcases.
2026-11-06T15:48:36.6746511Z   -nologo, --no-logo                   Run test(s), without displaying Microsoft Testplatform banner [default: True]
2026-11-06T15:48:36.6746757Z   -c, --configuration <CONFIGURATION>  The configuration to use for running tests. The default for most projects is 'Debug'.
2026-11-06T15:48:36.6747093Z   -f, --framework <FRAMEWORK>          The target framework to run tests for. The target framework must also be specified in the project file.
2026-11-06T15:48:36.6747514Z   --no-restore                         Do not restore the project before building. [default: False]
2026-11-06T15:48:36.6747712Z   --interactive                        Allows the command to stop and wait for user input or action (for example to complete authentication). [default: False]
2026-11-06T15:48:36.6747998Z   -v, -verbosity <LEVEL>               Set the MSBuild verbosity level. Allowed values are q[uiet], m[inimal], n[ormal], d[etailed], and diag[nostic].
2026-11-06T15:48:36.6748191Z   -r, --runtime <RUNTIME_IDENTIFIER>   The target runtime to test for.
2026-11-06T15:48:36.6748343Z   -a, --arch <ARCH>                    The target architecture.
2026-11-06T15:48:36.6748485Z   --os <OS>                            The target operating system.
2026-11-06T15:48:36.6748654Z   --disable-build-servers              Force the command to ignore any persistent build servers. [default: False]
2026-11-06T15:48:36.6748821Z   -?, -h, --help                       Show command line help.
2026-11-06T15:48:36.6748890Z 
2026-11-06T15:48:36.6749015Z Additional Arguments:
2026-11-06T15:48:36.6749156Z   Arguments passed to the application that is being run.
2026-11-06T15:48:36.6749227Z 
2026-11-06T15:48:36.7551498Z 
2026-11-06T15:48:36.7704709Z ##[error]Error: The process 'C:\Program Files\dotnet\dotnet.exe' failed with exit code 1
2026-11-06T15:48:36.7719425Z ##[warning]No test result files were found.
2026-11-06T15:48:36.7721805Z ##[warning].NET 5 has some compatibility issues with older Nuget versions(<=5.7), so if you are using an older Nuget version(and not dotnet cli) to restore, then the dotnet cli commands (e.g. dotnet build) which rely on such restored packages might fail. To mitigate such error, you can either: (1) - Use dotnet cli to restore, (2) - Use Nuget version 5.8 to restore, (3) - Use global.json using an older sdk version(<=3) to build
2026-11-06T15:48:36.7723613Z Info: Azure Pipelines hosted agents have been updated and now contain .Net 5.x SDK/Runtime along with the older .Net Core version which are currently lts. Unless you have locked down a SDK version for your project(s), 5.x SDK might be picked up which might have breaking behavior as compared to previous versions. You can learn more about the breaking changes here: https://docs.microsoft.com/en-us/dotnet/core/tools/ and https://docs.microsoft.com/en-us/dotnet/core/compatibility/ . To learn about more such changes and troubleshoot, refer here: https://docs.microsoft.com/en-us/azure/devops/pipelines/tasks/build/dotnet-core-cli?view=azure-devops#troubleshooting
2026-11-06T15:48:36.7725326Z ##[error]Dotnet command failed with non-zero exit code on the following projects : [
  'C:\\AG\\dev\\d_6\\_work\\10\\s\\AEL.Administradora.CargueDatosBDReferencia\\AEL.Administradora.CargueDatosBDReferencia.Test\\AEL.Administradora.CargueDatosBDReferencia.Test.csproj'
]
2026-11-06T15:48:36.7921598Z ##[section]Finishing: Ejecutar pruebas unitarias con cobertura
