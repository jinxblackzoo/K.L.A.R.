# Maintainer: jinx@blackzoo.de
pkgname=voll
pkgver=1.0.0
pkgrel=1
pkgdesc="V.O.L.L. - Vokabeln Ohne Langeweile Lernen"
arch=('any')
url="https://github.com/jinxblackzoo/V.O.L.L."
license=('GPL3')
depends=('python' 'gtk4' 'libadwaita' 'python-gobject' 'python-sqlalchemy' 'python-reportlab')
makedepends=('python-setuptools')
source=("git+$url.git")
sha256sums=('SKIP')

prepare() {
    cd "V.O.L.L."
    # Keine zusätzliche Vorbereitung nötig
}

build() {
    cd "V.O.L.L."
    python setup.py build
}

package() {
    cd "V.O.L.L."
    python setup.py install --root="$pkgdir" --optimize=1 --skip-build

    # Desktop-Datei installieren
    install -Dm644 "desktop/voll.desktop" "$pkgdir/usr/share/applications/voll.desktop"
    
    # Icon installieren
    install -Dm644 "desktop/voll.svg" "$pkgdir/usr/share/icons/hicolor/scalable/apps/voll.svg"
}
