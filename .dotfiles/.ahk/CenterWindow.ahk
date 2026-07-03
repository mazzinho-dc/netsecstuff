#Requires AutoHotkey v2.0

window_width_scale := 0.95
window_height_scale := 0.95

; Ermittelt den Monitor-Index, auf dem sich der Mittelpunkt des Fensters befindet.
; Fallback: primärer Monitor, falls aus irgendeinem Grund kein Treffer (sollte nicht vorkommen).
GetMonitorIndexFromWindow(hwnd)
{
    WinGetPos(&winX, &winY, &winW, &winH, hwnd)
    centerX := winX + winW / 2
    centerY := winY + winH / 2

    Loop MonitorGetCount()
    {
        MonitorGet(A_Index, &monLeft, &monTop, &monRight, &monBottom)
        if (centerX >= monLeft && centerX < monRight && centerY >= monTop && centerY < monBottom)
            return A_Index
    }
    return MonitorGetPrimary()
}

!Numpad0::
{
    activeWindow := "A"

    if !WinExist(activeWindow)
        return

    try
    {
        monitorIndex := GetMonitorIndexFromWindow(activeWindow)

        ; WorkArea statt vollen Monitor-Maßen verwenden, damit die Taskleiste
        ; nicht überdeckt wird. Falls das nicht gewünscht ist, MonitorGet()
        ; (ohne WorkArea) nutzen, um den vollen Monitorbereich zu nutzen.
        MonitorGetWorkArea(monitorIndex, &monLeft, &monTop, &monRight, &monBottom)
        monWidth := monRight - monLeft
        monHeight := monBottom - monTop

        newWidth := monWidth * window_width_scale
        newHeight := monHeight * window_height_scale
        newPosX := monLeft + (monWidth - newWidth) / 2
        newPosY := monTop + (monHeight - newHeight) / 2

        WinRestore(activeWindow)
        WinMove(newPosX, newPosY, newWidth, newHeight, activeWindow)
    }
    catch as err
    {
        ; z.B. Fenster wurde zwischen WinExist-Check und WinMove geschlossen
        ; oder verweigert Restore/Move (z.B. manche UWP-Apps) -> stillschweigend ignorieren
    }
}