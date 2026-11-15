# Signing and CI

## Gradle: signing from a properties file, version from CI

```groovy
// android/app/build.gradle — top of file
def signingProps = new Properties()
def signingFile = file(System.getenv('KEYSTORE_PROPERTIES') ?: '../keystore.properties')
if (signingFile.exists()) signingFile.withInputStream { signingProps.load(it) }

android {
    defaultConfig {
        // CI passes -PappVersionName=1.2.3 (from the git tag) and -PappVersionCode=10203.
        versionCode((project.findProperty('appVersionCode') ?: '1') as int)
        versionName project.findProperty('appVersionName') ?: "1.0.0"
    }
    signingConfigs {
        if (signingProps.storeFile) {
            release {
                storeFile file(signingProps.storeFile)
                storePassword signingProps.storePassword
                keyAlias signingProps.keyAlias
                keyPassword signingProps.keyPassword
            }
        }
    }
    buildTypes {
        release { if (signingProps.storeFile) signingConfig signingConfigs.release }
    }
}
```

Gitignore `android/keystore.properties` and `*.jks`. If the user's repo already has a `-PccVersionCode`-style prefix, keep theirs.


## versionCode scheme

`MAJOR*10000 + MINOR*100 + PATCH` → `1.0.2` = `10002`. Play rejects any upload whose versionCode is not higher than every earlier upload on any track, so never reuse or lower it. A tag `v1.0.2-rc1` gets the same code as `v1.0.2`; only upload one of them to Play.

## Secrets

| Secret | Value |
|--------|-------|
| `KEYSTORE_BASE64` | `base64 -w0 app-release.jks` |
| `KEYSTORE_PASSWORD` | store password |
| `KEY_PASSWORD` | key password |
| `KEY_ALIAS` | alias |

Set them without exposing values: `gh secret set KEYSTORE_PASSWORD < <(grep '^storePassword=' keystore.properties | cut -d= -f2-)`.
If several `gh` accounts are logged in, select the one that owns the repo with `GH_TOKEN=$(gh auth token --user <owner>)`.

## Verifying a build

```bash
bt="$ANDROID_HOME/build-tools/$(ls "$ANDROID_HOME/build-tools" | sort -V | tail -n1)"
"$bt/apksigner" verify --print-certs app-release.apk | grep "SHA-256"
jarsigner -verify app-release.aab | grep "jar verified"
"$bt/aapt2" dump badging app-release.apk | grep -E "^package|uses-permission"
```

The APK cert SHA-256 must equal the keystore's. Once Play App Signing uses your own key, Play's "App signing key certificate" SHA-256 equals it too, so website APKs and Play installs update each other.

## PEPK details

- Download both `pepk.jar` and `encryption_public_key.pem` from the Play App signing dialog; the `.pem` is unique to the app.
- Needs Java 11+. If the system has none, a portable JDK (Temurin zip) in the signing folder works.
- Run with `--rsa-aes-encryption` (current Play default). Older `--encryptionkey=` hex mode is for the legacy dialog only.
- PEPK prompts for the store password then the key password. Pipe them from `keystore.properties` with `printf '%s\n%s\n' "$sp" "$kp" | java -jar pepk.jar ...`.
- Output ZIP goes to "Upload generated ZIP"; then Save. The page then shows the app signing and upload key certificates.

## Website APK alongside Play

Publish the signed release APK to the project's own site/GitHub Release from the same tag. Same key = same app identity, so a website install can later be updated from Play (versionCode must be higher). Serve the APK with `Content-Type: application/vnd.android.package-archive` and `Content-Disposition: attachment` so it downloads instead of opening.
