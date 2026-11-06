  - task: SonarQubePrepare@5
    displayName: Prepare analysis on SonarQube
    inputs:
      SonarQube: c920b15f-1de4-45cf-8de8-00186bd2439a
      scannerMode: 'MSBuild'
      projectKey: '$(sonarProject)'
      projectName: '$(sonarProject)'
      projectVersion: '$(Build.BuildNumber)_$(Build.SourceBranchName)'
      extraProperties: |
        sonar.exclusions=**/bin/**,**/obj/**
        sonar.coverage.exclusions=**/Program.cs,**/*.Test/**
        sonar.cs.opencover.reportsPaths=$(Agent.TempDirectory)/TestResults/**/coverage.opencover.xml
        sonar.scm.provider=git
