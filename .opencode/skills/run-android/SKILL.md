---
name: run-android
description: Use when the user wants to run or debug the Android companion app. Trigger on "android", "apk", "app", "mobile", "android studio", "chay android", "xay dung apk". The Android app receives IoT data via BLE.
---

# Run Android App

## Quick Start

1. Open `android/` folder in Android Studio
2. Sync Gradle (File → Sync Project with Gradle Files)
3. Run on emulator or device (Shift+F10)

## Files

| File | Purpose |
|------|---------|
| `android/app/build.gradle` | App build config |
| `android/build.gradle` | Project build config |
| `android/gradle.properties` | Gradle properties |
| `android/app/src/main/` | Source code |

## Requirements

- Android Studio Arctic Fox or later
- JDK 11+
- Android SDK 30+

## Build APK

```cmd
cd C:\ĐATN\android
gradlew assembleDebug
```

APK output: `android/app/build/outputs/apk/debug/app-debug.apk`

## Features

- BLE connection to ESP32 gateway
- Display real-time sensor data
- Local SQLite storage
- Data visualization

## Gradle Commands

```cmd
# Clean project
gradlew clean

# Build debug APK
gradlew assembleDebug

# Build release APK
gradlew assembleRelease

# Run tests
gradlew test

# Install on device
gradlew installDebug
```

## Common Issues

### Gradle Sync Fails
1. Check Android Studio SDK version
2. File → Sync Project with Gradle Files
3. Invalidate Caches → Restart

### BLE Not Working
1. Ensure location permissions granted
2. Check Bluetooth is enabled
3. Verify ESP32 is advertising

### Build Error
```cmd
cd C:\ĐATN\android
gradlew clean
gradlew assembleDebug
```

### SDK Not Found
1. File → Project Structure → SDK Location
2. Set Android SDK path

## Android Permissions

```xml
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
```

## Project Structure

```
android/
├── app/
│   ├── build.gradle
│   └── src/
│       └── main/
│           ├── AndroidManifest.xml
│           ├── java/
│           │   └── com/example/iotapp/
│           │       ├── MainActivity.kt
│           │       ├── BLEManager.kt
│           │       └── DatabaseHelper.kt
│           └── res/
│               ├── layout/
│               └── values/
├── build.gradle
├── gradle.properties
└── settings.gradle
```