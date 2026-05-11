param(
    [string]$PptxPath = "D:\45_pyCycle_edu\docs\slides\pycycle_ai_prompting_course.pptx",
    [string]$OutputDir = "D:\45_pyCycle_edu\docs\slides\preview_png",
    [int]$Width = 1600,
    [int]$Height = 900
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $PptxPath)) {
    throw "PPTX not found: $PptxPath"
}

Remove-Item -Recurse -Force -LiteralPath $OutputDir -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$powerPoint = New-Object -ComObject PowerPoint.Application
try {
    $presentation = $powerPoint.Presentations.Open($PptxPath, $false, $false, $false)
    $slideCount = $presentation.Slides.Count
    $presentation.Export($OutputDir, "PNG", $Width, $Height)
    $presentation.Close()
}
finally {
    $powerPoint.Quit()
}

$files = Get-ChildItem -LiteralPath $OutputDir -Filter "*.PNG" | Sort-Object Name
Write-Output "Exported $($files.Count) preview images from $slideCount slides to $OutputDir"
Write-Output "Manual visual check required:"
Write-Output "- Text must stay inside frames and must not be clipped."
Write-Output "- Images must preserve aspect ratio and must not look stretched."
Write-Output "- Text must be readable for classroom projection and older students."
Write-Output "- Slides should be visually balanced, with enough images and not only text."

