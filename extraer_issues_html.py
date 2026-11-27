steps:
- task: SonarSource.sonarqube.15B84CA1-B62F-4A2A-A403-89B77A063157.SonarQubePrepare@8
  displayName: 'Prepare analysis on SonarQube Server'
  inputs:
    SonarQube: sonarpasarela
    projectKey: AEL.PasarelaPagos.Quality
    projectName: 'AEL.PasarelaPagos:Quality'
    projectVersion: '$(Build.BuildNumber)_$(Build.SourceBranchName)'
    extraProperties: |
     sonar.cs.opencover.reportsPaths=$(System.DefaultWorkingDirectory)/TestResults/coverage.opencover.xml
     sonar.scanner.metadataFilePath=$(Agent.TempDirectory)/sonar/$(Build.BuildNumber)/test/report-task.txt
     sonar.exclusions=**/bin/**,**/obj/**,**/packages/**,**/Service References/**,**/Azure/**,**/Proveedores/AvalPay/MafaS37/**,**/Transacciones**/
     sonar.coverage.exclusions=**/*Test*/**,**/Program.cs,**/Startup.cs,Azure,Proveedores/AvalPay/MafaS37
     sonar.qualitygate.wait=false
     sonar.inclusions=src/**
