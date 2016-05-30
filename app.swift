#!/usr/bin/env swift

import AppKit

func setWallpaper(wallpaperPath: String) {
    let sharedWorkspace = NSWorkspace.sharedWorkspace()
    let mainScreen = NSScreen.mainScreen()
    let wallpaperUrl : NSURL = NSURL.fileURLWithPath(wallpaperPath)
    do {
        try sharedWorkspace.setDesktopImageURL(wallpaperUrl, forScreen: mainScreen!, options: [:])
    } catch (let error) {
        print(error)
    }
}

if Process.arguments.count == 2 {
    let wallpaperPath = Process.arguments[1]
    setWallpaper(wallpaperPath)
} else {
    print("Usage: \(Process.arguments[0]) WALLPAPER")
}
