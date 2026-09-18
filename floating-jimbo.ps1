Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$root = $PSScriptRoot
$launcher = Join-Path $root 'start.bat'
$backend = Join-Path $root 'backend\app'
$python = Join-Path $root 'backend\venv\Scripts\python.exe'
$url = 'http://localhost:4149'
$chromium = 'C:\Users\Bonzo2\AppData\Local\Chromium\Application\chrome.exe'

function Open-InBrowserOS {
    param([string]$target)
    if (Test-Path $chromium) {
        Start-Process $chromium -ArgumentList "--new-tab $target --profile-directory=Default"
    } else {
        Start-Process $target
    }
}

function Test-Backend {
    try {
        $r = Invoke-WebRequest -Uri "$url/api/health" -UseBasicParsing -TimeoutSec 2
        return $r.StatusCode -eq 200
    } catch { return $false }
}

function Start-BackendHidden {
    if (-not (Test-Path $python)) { return $false }
    $env:PORT = '4149'
    Start-Process -FilePath $python -ArgumentList 'main.py' -WorkingDirectory $backend -WindowStyle Hidden
    return $true
}

if (-not (Test-Backend)) {
    [void](Start-BackendHidden)
    Start-Sleep -Seconds 2
}

$form = New-Object System.Windows.Forms.Form
$form.FormBorderStyle = [System.Windows.Forms.FormBorderStyle]::None
$form.StartPosition = [System.Windows.Forms.FormStartPosition]::Manual
$form.Size = New-Object System.Drawing.Size(54,54)
$form.BackColor = [System.Drawing.Color]::FromArgb(12,18,34)
$form.TopMost = $true
$form.ShowInTaskbar = $false
$form.Opacity = 0.92

$screen = [System.Windows.Forms.Screen]::AllScreens[0].WorkingArea
$form.Location = New-Object System.Drawing.Point(($screen.Left + 20), ($screen.Bottom - 90))

$iconPath = 'Z:\MCPu\Iconsmkj7767hh7676\6396b9ab03d53e758d0127e523445d8d.windows\icon_48x48.png'
if (-not (Test-Path $iconPath)) {
    # fallback do lokalnej kopii
    $iconPath = 'T:\Browser_Bonzo_Extencion\icons_all\icon_48x48.png'
}
$iconImg = [System.Drawing.Image]::FromFile($iconPath)

$btn = New-Object System.Windows.Forms.Button
$btn.Text = ''
$btn.Image = $iconImg
$btn.ImageAlign = [System.Drawing.ContentAlignment]::MiddleCenter
$btn.Dock = [System.Windows.Forms.DockStyle]::Fill
$btn.FlatStyle = [System.Windows.Forms.FlatStyle]::Flat
$btn.FlatAppearance.BorderSize = 1
$btn.FlatAppearance.BorderColor = [System.Drawing.Color]::FromArgb(126,142,255)
$btn.BackColor = [System.Drawing.Color]::FromArgb(20,30,58)
$btn.add_Click({
    if (-not (Test-Backend)) {
        [void](Start-BackendHidden)
        Start-Sleep -Seconds 1
    }
    Open-InBrowserOS $url
})
$form.Controls.Add($btn)

$drag = $false
$start = $null
$origin = $null
$form.Add_MouseDown({ param($s,$e) if ($e.Button -eq [System.Windows.Forms.MouseButtons]::Left) { $script:drag = $true; $script:start = [System.Windows.Forms.Cursor]::Position; $script:origin = $form.Location } })
$form.Add_MouseMove({ if ($script:drag) { $p=[System.Windows.Forms.Cursor]::Position; $dx=$p.X-$script:start.X; $dy=$p.Y-$script:start.Y; $form.Location = New-Object System.Drawing.Point($script:origin.X+$dx,$script:origin.Y+$dy) } })
$form.Add_MouseUp({ $script:drag = $false })

$ctx = New-Object System.Windows.Forms.ContextMenuStrip
$openItem = $ctx.Items.Add('Open JIMBO')
$openItem.add_Click({ Open-InBrowserOS $url })
$startItem = $ctx.Items.Add('Restart Backend')
$startItem.add_Click({ [void](Start-BackendHidden) })
$exitItem = $ctx.Items.Add('Exit Button')
$exitItem.add_Click({ $form.Close() })
$form.ContextMenuStrip = $ctx

[System.Windows.Forms.Application]::Run($form)
