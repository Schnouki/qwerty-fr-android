# QWERTY-fr for Android

This is a port of the [QWERTY-fr keyboard layout](https://github.com/qwerty-fr/qwerty-fr) for Android. By installing this app, you will be able to use that layout **on external, physical keyboards** (either USB-C or Bluetooth).

## Limitations

Android keyboard layouts are more limited than most other platforms. This means that QWERTY-fr for Android has less features than on Windows, Mac or Linux. In particular, there are only dead keys for common accents (only acute, grave, diaresis, circumflex, and tilde), and not for Greek letters or math symbols.

## How to use it?

1. Download the APK from <https://github.com/Schnouki/qwerty-fr-android/releases>
2. Install the APK: you can either transfer it to your Android device and install it from there, or use `adb install qwerty-fr.apk` if you know how to use ADB.
3. Connect your keyboard
4. Change the layout to QWERTY-fr. The exact process to do it varies by device; for me, I have to go into Settings > System & Updates > Language & input > More settings > Physical keyboard > (Keyboard name & model), disable the default layout, and choose "English (US), QWERTY-fr" from the list.

## How to build it?

1. Generate an up-to-date `.kcm` file: `make qwerty-fr.kcm` (requires Python3, curl, and `libxkbcommon`)
2. Build the app:
  - Using Docker (easy if you don't have Android SDK and build tools installed): `make docker-debug`
  - Using Gradle (if you have Android SDK and build tools installed and ready): `make debug`

The output will be in `app/build/outputs/apk`.

## About this Android app

This app is heavily based on the [Custom Keyboard Layout](https://github.com/ris58h/custom-keyboard-layout/) app by [Ilya Rodionov](https://github.com/ris58h). Many thanks to him for that! 🙏
