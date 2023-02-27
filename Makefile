QWERTY_FR_VERSION = 0.7.2

DEBUG_APK = app/build/outputs/apk/debug/app-debug.apk
RELEASE_APK = app/build/outputs/apk/release/app-release.apk

DOCKER_IMAGE = redemonbr/android-sdk:api-33

all: help

.PHONY: help clean debug release docker-debug docker-release
help:
	@echo "Usage:"
	@echo "  make qwerty-fr.kcm   Generate an up-to-date KCM file based on QWERTY-fr v$(QWERTY_FR_VERSION)"
	@echo "  make debug           Build a debug APK using local Android build tools"
	@echo "  make docker-debug    Build a debug APK using Docker"
	@echo "  make clean           Clean all generated files"
	@echo ""
	@echo "If you have a release keystore:"
	@echo "  make release         Build a release APK using local Android build tools"
	@echo "  make docker-release  Build a release APK using Docker"

clean:
	rm -rf qwerty-fr.kcm .gradle/ app/build/

debug: $(DEBUG_APK)
release: $(RELEASE_APK)

$(DEBUG_APK): qwerty-fr.kcm app/build.gradle $(shell find app/src -type f)
	./gradlew assembleDebug

$(RELEASE_APK): qwerty-fr.kcm app/build.gradle $(shell find app/src -type f)
	./gradlew assembleRelease

docker-debug: qwerty-fr.kcm
	docker run --rm --volume $(PWD):/app --workdir /app \
		--env ASDK_ACCEPT_LICENSES=yes --env ASDK_ACCEPT_LICENSES_SILENT=yes \
		$(DOCKER_IMAGE) \
		./gradlew assembleDebug

docker-release: qwerty-fr.kcm
	docker run --rm --volume $(PWD):/app --workdir /app \
		--env ASDK_ACCEPT_LICENSES=yes --env ASDK_ACCEPT_LICENSES_SILENT=yes \
		$(DOCKER_IMAGE) \
		./gradlew assembleRelease

qwerty-fr.kcm:
	curl -sL "https://github.com/qwerty-fr/qwerty-fr/raw/v$(QWERTY_FR_VERSION)/linux/us_qwerty-fr" \
		| ./xkb2kcm.py > $@
