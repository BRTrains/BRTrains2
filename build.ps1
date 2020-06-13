<#
.SYNOPSIS
	Builds the grf file.
	
.DESCRIPTION
	Compiles the project into a grf file, optionally starting the game.
	
.PARAMETER ProjectName
	The name of the file to create when compiling the grf.
	
.PARAMETER StartGame
	This switch will, if already running close openttd, copy over the compiled grf file,
	and restart the game again.
	
.PARAMETER SkipChecks
	Skip project folder/file validations.
	
.PARAMETER srcDirectory
	The relative path pointing to the folder containing the logic code.
	
.PARAMETER gfxDirectory
	The relative path pointing to the folder containing all the graphic files.
	
.PARAMETER langDirectory
	The relative path pointing to the folder containing the language files.
	
.PARAMETER buildDirectory
	The relative path pointing to the folder where the build .nml and .grf files will be created.
	
.EXAMPLE
	PS C:\> .\build.ps1 -ProjectName "test" -StartGame
	
	This will compile a grf to the default path .\build\test.grf and start the openttd client.
	
.INPUTS
	None
	
.OUTPUTS
	None
	
.NOTES
	All of the parameters allow for default values so that you don't have to type out the parameters manually.
	Edit this file to configure these defaults.
	
#>
[CmdletBinding()]
param (
	
	[Parameter()]
	[string]
	$ProjectName = "mukts",
	
	[Parameter()]
	[switch]
	$StartGame,
	
	[Parameter()]
	[switch]
	$SkipChecks,
	
	[Parameter()]
	[string]
	$srcDirectory = "src",
	
	[Parameter()]
	[string]
	$gfxDirectory = "gfx",
	
	[Parameter()]
	[string]
	$langDirectory = "lang",
	
	[Parameter()]
	[string]
	$buildDirectory = "build"
	
)

function Test-ProjectStructure {
	
	[CmdletBinding()]
	param (
		
		[Parameter()]
		[string]
		$srcDirectory,
		
		[Parameter()]
		[string]
		$gfxDirectory,
		
		[Parameter()]
		[string]
		$langDirectory
		
	)
	
	# Ensure that the filepaths provided are valid
	Write-Verbose "Checking required folders exist."	
	
	if ((Test-Path -Path $srcDirectory) -eq $false) {
		
		Write-Error "The source directory: $srcDirectory could not be found."
		throw
		
	}
	if ((Test-Path -Path $gfxDirectory) -eq $false) {
		
		Write-Error "The graphics directory: $gfxDirectory could not be found."
		throw
		
	}
	if ((Test-Path -Path $langDirectory) -eq $false) {
		
		Write-Error "The language directory: $langDirectory could not be found."
		throw
		
	}
	
	# Check that some required files are present
	Write-Verbose "Checking necessary files are present."
	
	if ((Test-Path -Path (Join-Path -Path $srcDirectory -ChildPath "grf.pnml")) -eq $false) {
		
		Write-Error "The main grf.pnml file could not be found in $srcDirectory. This file must be present."
		throw
		
	}
	if ((Test-Path -Path (Join-Path -Path $srcDirectory -ChildPath "railtypes.pnml")) -eq $false) {
		
		Write-Error "The definition railtypes.pnml file could not be found in the $srcDirectory. This file must be present."
		throw
		
	}
	if ((Test-Path -Path (Join-Path -Path $srcDirectory -ChildPath "templates.pnml")) -eq $false) {
		
		Write-Warning "The definition templates.pnml file was not found. It is highly recommended to put template definitions into this file."
		
	}
	
	Write-Verbose "The project structure is correct."
	
	
}

# ==Main function==

# Check that there's a config file.
$configFile = Join-Path -Path $PSScriptRoot -ChildPath "conf.ps1"
if ((Test-Path -Path $configFile) -eq $false) {
	
	$confString = "`# Point this to the openttd executable`n`$config_OpenttdExecutablePath = `"`"`n`# Point this to the openttd user folder`n`$config_OpenttdUserDataPath = `"`""
	Out-File -InputObject $confString -FilePath $configFile -Force
	
	Write-Error "First time running script. Please fill in the configuration file located at $configFile"
	return
	
}

# Load the config file in
. $configFile

# Resolve the paths from relative to absolute
$srcDirectory = Join-Path -Path $PSScriptRoot -ChildPath $srcDirectory
$gfxDirectory = Join-Path -Path $PSScriptRoot -ChildPath $gfxDirectory
$langDirectory = Join-Path -Path $PSScriptRoot -ChildPath $langDirectory
$buildDirectory = Join-Path -Path $PSScriptRoot -ChildPath $buildDirectory

# Run validation on project structure
if ($SkipChecks -eq $false) {	
	try {
		
		Test-ProjectStructure -srcDirectory $srcDirectory -gfxDirectory $gfxDirectory -langDirectory $langDirectory
		
	}catch {
		
		return
		
	}
}

# Get list of all .pnml files aside from the special ones
$pnmlFiles = Get-ChildItem -Path $PSScriptRoot -Recurse -Include "*.pnml" -Exclude "grf.pnml","railtypes.pnml","templates.pnml"
Write-Verbose "Found $($pnmlFiles.Count) .pnml files."
$pnmlFiles | Write-Verbose

# First take the contents of special .pnml files and put them into the master file
Write-Verbose "Merging together special .pnml files."
$nmlContent += Get-Content -Path (Join-Path -Path $srcDirectory -ChildPath "grf.pnml")
$nmlContent += Get-Content -Path (Join-Path -Path $srcDirectory -ChildPath "railtypes.pnml")
if ((Test-Path -Path (Join-Path -Path $srcDirectory -ChildPath "templates.pnml")) -eq $true) {
	
	$nmlContent += Get-Content -Path (Join-Path -Path $srcDirectory -ChildPath "templates.pnml")
	
}

# Now take the contents of the rest .pnml files and put them into the master file
Write-Verbose "Merging together all other .pnml files."
$pnmlFiles | ForEach-Object {
	$nmlContent += Get-Content -Path $_.FullName
}

# Write the master nml file to disk, overwrite any existing file
Write-Verbose "Writing master nml file to: $buildDirectory"
Out-File -InputObject $nmlContent -FilePath (Join-Path -Path $buildDirectory -ChildPath "$ProjectName.nml") -Force

# Compile the nml to a grf
Write-Verbose "Compiling nml to grf file."
try {
	
	Start-Process nmlc -ArgumentList "--lang", $langDirectory, "--grf", (Join-Path -Path $buildDirectory -ChildPath "$ProjectName.grf"),`
		(Join-Path -Path $buildDirectory -ChildPath "$ProjectName.nml") -Wait -NoNewWindow
	
}catch [System.InvalidOperationException]{
	
	Write-Error "The nml binary could not be located.`nCheck to make sure it is in PATH or alternatively install it by running: pip install nml"
	return
	
}catch {
	
	Write-Error "There was an issue in compiling the .nml to a .grf file."
	return
	
}

# Optionally, (re)start the game
if ($StartGame -eq $true) {
	Write-Verbose "Copying over grf file and restarting the game."
	
	# Kill existing openttd window
	Stop-Process -Name "OpenTTD*" -Force -ErrorAction SilentlyContinue
	
	# Copy over the grf to the openttd user folder
	Copy-Item -Path (Join-Path -Path $buildDirectory -ChildPath "$ProjectName.grf") -Destination `
		(Join-Path -Path $config_OpenttdUserDataPath -ChildPath "newgrf") -Force
	
	# Start openttd again
	Start-Process -FilePath $config_OpenttdExecutablePath
	
}

