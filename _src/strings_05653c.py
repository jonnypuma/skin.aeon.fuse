# -*- coding: utf-8 -*-
"""0.56.53 strings, all 23 languages: what the Aeon Fuse Waveform Visualizer adds (Recommended add-ons, helper 0.3.115:
the build for this device, visualization.aeonwave.<platform>). Repeatable."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import strings_05653 as base  # noqa: E402

IDS = [32797]
EN = ['A calm, thin waveform on the Now playing card, drawn in the skin\'s own box and smoothed so loud passages do not spike. The build for this device is installed.']
T = {
    'cs_cz': ['Klidná tenká vlna na kartě Právě hraje, kreslená v rámečku vzhledu a vyhlazená, aby hlasité pasáže nevystřelovaly. Nainstaluje se verze pro toto zařízení.'],
    'da_dk': ['En rolig, tynd bølgeform på kortet Afspiller nu, tegnet i skinnets egen boks og udglattet, så høje passager ikke giver spidser. Versionen til denne enhed installeres.'],
    'de_de': ['Eine ruhige, dünne Wellenform auf der Wiedergabe-Karte, im Rahmen des Skins gezeichnet und geglättet, damit laute Stellen nicht ausschlagen. Die Version für dieses Gerät wird installiert.'],
    'el_gr': ['Μια ήρεμη, λεπτή κυματομορφή στην κάρτα Αναπαραγωγή τώρα, στο πλαίσιο του κελύφους, εξομαλυμένη ώστε τα δυνατά σημεία να μην πετάγονται. Εγκαθίσταται η έκδοση για αυτή τη συσκευή.'],
    'es_es': ['Una onda fina y tranquila en la tarjeta En reproducción, dibujada en el recuadro de la piel y suavizada para que los pasajes fuertes no se disparen. Se instala la versión para este dispositivo.'],
    'fi_fi': ['Rauhallinen, ohut aaltomuoto Nyt toistetaan -kortilla, ulkoasun omassa laatikossa ja tasoitettuna, jotta kovat kohdat eivät piikkaa. Tämän laitteen versio asennetaan.'],
    'fr_fr': ['Une onde fine et calme sur la carte Lecture en cours, dessinée dans le cadre du skin et lissée pour que les passages forts ne fassent pas de pics. La version pour cet appareil est installée.'],
    'hu_hu': ['Nyugodt, vékony hullámforma a Most játszott kártyán, a felszín saját keretében, kisimítva, hogy a hangos részek ne ugorjanak ki. Az eszköznek megfelelő változat települ.'],
    'it_it': ['Una forma d’onda sottile e calma sulla scheda In riproduzione, disegnata nel riquadro della skin e smussata perché i passaggi forti non facciano picchi. Viene installata la versione per questo dispositivo.'],
    'ja_jp': ['再生中カードに表示される、細く落ち着いた波形。スキンの枠内に描かれ、大きな音でも尖らないよう滑らかにします。このデバイス用のビルドがインストールされます。'],
    'ko_kr': ['재생 중 카드에 표시되는 가늘고 차분한 파형. 스킨의 상자 안에 그려지고 큰 소리에도 튀지 않게 부드럽게 다듬습니다. 이 기기에 맞는 빌드가 설치됩니다.'],
    'nb_no': ['En rolig, tynn bølgeform på kortet Spilles nå, tegnet i skallets egen boks og glattet så høye partier ikke gir topper. Versjonen for denne enheten installeres.'],
    'nl_nl': ['Een rustige, dunne golfvorm op de kaart Nu afgespeeld, getekend in het kader van de skin en afgevlakt zodat harde passages niet uitschieten. De versie voor dit apparaat wordt geïnstalleerd.'],
    'pl_pl': ['Spokojna, cienka fala na karcie Teraz odtwarzane, rysowana w ramce skórki i wygładzona, by głośne fragmenty nie strzelały w górę. Instalowana jest wersja dla tego urządzenia.'],
    'pt_br': ['Uma onda fina e calma no cartão Tocando agora, desenhada no quadro da skin e suavizada para que trechos altos não disparem. A versão para este aparelho é instalada.'],
    'pt_pt': ['Uma onda fina e calma no cartão A reproduzir, desenhada no quadro da skin e suavizada para que passagens altas não disparem. É instalada a versão para este dispositivo.'],
    'ru_ru': ['Спокойная тонкая волна на карточке «Сейчас играет», в рамке оболочки, сглаженная, чтобы громкие места не давали пиков. Устанавливается сборка для этого устройства.'],
    'sv_se': ['En lugn, tunn vågform på kortet Spelas nu, ritad i skalets egen ruta och utjämnad så att starka partier inte ger toppar. Versionen för den här enheten installeras.'],
    'tr_tr': ['Şimdi çalıyor kartında, görünümün kendi kutusunda çizilen ve yüksek bölümlerde sıçramasın diye yumuşatılan ince, sakin bir dalga. Bu cihaza uygun sürüm kurulur.'],
    'uk_ua': ['Спокійна тонка хвиля на картці «Зараз грає», у рамці оболонки, згладжена, щоб гучні місця не давали піків. Встановлюється збірка для цього пристрою.'],
    'zh_cn': ['正在播放卡片上细而平稳的波形，绘制在皮肤自带的框内，并经过平滑，响亮段落不会出现尖峰。将安装适合此设备的版本。'],
    'zh_tw': ['正在播放卡片上細而平穩的波形，繪製在外觀自帶的框內，並經過平滑，響亮段落不會出現尖峰。將安裝適合此裝置的版本。'],
}

if __name__ == '__main__':
    base.IDS, base.EN, base.T = IDS, EN, T
    base.main()
