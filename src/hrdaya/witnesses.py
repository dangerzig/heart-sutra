"""
Witness catalog for the Heart Sūtra critical edition.

This module defines all known witnesses organized by tradition,
following Conze (1967), Nattier (1992), and subsequent scholarship.
"""

from typing import Optional
from .models import Witness, WitnessType, Script


# =============================================================================
# CHINESE WITNESSES
# =============================================================================

CHINESE_WITNESSES = {
    # Taishō Canon versions
    "T250": Witness(
        id="T250",
        name="摩訶般若波羅蜜大明咒經 (Móhē bōrě bōluómì dàmíng zhòu jīng)",
        witness_type=WitnessType.CHINESE,
        date="402-412 CE",
        date_circa=True,
        location="Taishō Tripiṭaka Vol. 8, No. 250",
        provenance="China",
        script=Script.TRADITIONAL_CHINESE,
        edition_used="Taishō Shinshū Daizōkyō",
        description="Attributed to Kumārajīva. Long version. May be spurious attribution.",
        scholarly_refs=["Nattier 1992", "Tanahashi 2014"],
    ),
    "T251": Witness(
        id="T251",
        name="般若波羅蜜多心經 (Bōrě bōluómìduō xīn jīng)",
        witness_type=WitnessType.CHINESE,
        date="649 CE",
        date_circa=False,
        location="Taishō Tripiṭaka Vol. 8, No. 251",
        provenance="China",
        script=Script.TRADITIONAL_CHINESE,
        edition_used="Taishō Shinshū Daizōkyō",
        description="Attributed to Xuanzang (玄奘). Short version. "
                    "Most widely used Chinese recension. Analytical base text.",
        scholarly_refs=["Nattier 1992", "Fukui 1987"],
    ),
    "T252": Witness(
        id="T252",
        name="般若波羅蜜多心經 (Bōrě bōluómìduō xīn jīng)",
        witness_type=WitnessType.CHINESE,
        date="c. 700 CE",
        date_circa=True,
        location="Taishō Tripiṭaka Vol. 8, No. 252",
        provenance="China",
        script=Script.TRADITIONAL_CHINESE,
        edition_used="Taishō Shinshū Daizōkyō",
        description="Attributed to Kumārajīva. Alternate short version.",
        scholarly_refs=["Nattier 1992"],
    ),
    "T253": Witness(
        id="T253",
        name="般若波羅蜜多心經 (Bōrě bōluómìduō xīn jīng)",
        witness_type=WitnessType.CHINESE,
        date="c. 700-730 CE",
        date_circa=True,
        location="Taishō Tripiṭaka Vol. 8, No. 253",
        provenance="China",
        script=Script.TRADITIONAL_CHINESE,
        edition_used="Taishō Shinshū Daizōkyō",
        description="Attributed to Fayue (法月). Long version with frame narrative.",
        scholarly_refs=["Nattier 1992"],
    ),
    "T254": Witness(
        id="T254",
        name="普遍智藏般若波羅蜜多心經 (Pǔbiàn zhìzàng bōrě bōluómìduō xīn jīng)",
        witness_type=WitnessType.CHINESE,
        date="c. 733 CE",
        date_circa=True,
        location="Taishō Tripiṭaka Vol. 8, No. 254",
        provenance="China",
        script=Script.TRADITIONAL_CHINESE,
        edition_used="Taishō Shinshū Daizōkyō",
        description="Attributed to Prajñā (般若). Long version.",
        scholarly_refs=["Nattier 1992"],
    ),
    "T255": Witness(
        id="T255",
        name="般若波羅蜜多心經 (Bōrě bōluómìduō xīn jīng)",
        witness_type=WitnessType.CHINESE,
        date="c. 790 CE",
        date_circa=True,
        location="Taishō Tripiṭaka Vol. 8, No. 255",
        provenance="China",
        script=Script.TRADITIONAL_CHINESE,
        edition_used="Taishō Shinshū Daizōkyō",
        description="Attributed to Prajñācakra (智慧輪). Long version.",
        scholarly_refs=["Nattier 1992"],
    ),
    "T256": Witness(
        id="T256",
        name="般若波羅蜜多心經 (唐梵翻對字音)",
        witness_type=WitnessType.CHINESE,
        date="c. 7th-8th century CE",
        date_circa=True,
        location="Taishō Tripiṭaka Vol. 8, No. 256",
        provenance="China",
        script=Script.TRADITIONAL_CHINESE,
        edition_used="Taishō Shinshū Daizōkyō",
        description="Sanskrit text transliterated into Chinese characters. "
                    "Critical for understanding Sanskrit ← Chinese relationship.",
        scholarly_refs=["Nattier 1992", "Attwood 2017"],
    ),
    "T257": Witness(
        id="T257",
        name="佛說聖佛母般若波羅蜜多經 (Fó shuō shèng fómǔ bōrě bōluómìduō jīng)",
        witness_type=WitnessType.CHINESE,
        date="1005 CE",
        date_circa=False,
        location="Taishō Tripiṭaka Vol. 8, No. 257",
        provenance="China (Song dynasty translation)",
        script=Script.TRADITIONAL_CHINESE,
        edition_used="Taishō Shinshū Daizōkyō",
        description="Dānapāla (施護) translation from Sanskrit long recension. "
                    "Includes oṃ in mantra and full frame narrative.",
        scholarly_refs=["Nattier 1992", "Attwood 2021a", "Attwood 2024"],
    ),
    # Dunhuang manuscripts
    "S2464": Witness(
        id="S2464",
        name="Stein Collection S. 2464",
        witness_type=WitnessType.CHINESE,
        date="c. 600-700 CE",
        date_circa=True,
        location="British Library",
        provenance="Dunhuang",
        script=Script.TRADITIONAL_CHINESE,
        description="Early Dunhuang manuscript. Corresponds to T256 (transliterated Sanskrit).",
        scholarly_refs=["Nattier 1992"],
    ),
    # Source text (Large Prajñāpāramitā)
    "T223": Witness(
        id="T223",
        name="摩訶般若波羅蜜經 (Large Prajñāpāramitā)",
        witness_type=WitnessType.SOURCE,
        date="404 CE",
        date_circa=False,
        location="Taishō Vol. 8, No. 223",
        provenance="China",
        script=Script.TRADITIONAL_CHINESE,
        description="Kumārajīva's translation of Large PP (corresponding to 25,000 lines). "
                    "Primary source from which Heart Sūtra core was extracted.",
        scholarly_refs=["Nattier 1992"],
    ),
}


# =============================================================================
# SANSKRIT WITNESSES
# =============================================================================

SANSKRIT_WITNESSES = {
    # Japanese witnesses (from Conze's notation)
    "Ja": Witness(
        id="Ja",
        name="Hōryū-ji Palm-leaf Manuscript",
        witness_type=WitnessType.SANSKRIT,
        date="c. 8th century CE",
        date_circa=True,
        location="Tokyo National Museum (via Hōryū-ji Temple)",
        provenance="India → Japan",
        material="Palm leaf",
        script=Script.SIDDHAM,
        first_published="Müller 1881",
        description="Earliest undated Sanskrit manuscript. Traditional date 609 CE "
                    "is unreliable (Bühler, Nattier). Short text version. "
                    "Contains significant scribal errors.",
        scholarly_refs=["Müller 1881", "Conze 1967", "Nattier 1992"],
    ),
    "Jb": Witness(
        id="Jb",
        name="Hase-ji Manuscript (Long Text)",
        witness_type=WitnessType.SANSKRIT,
        date="c. 9th century CE",
        date_circa=True,
        location="Japan",
        provenance="China → Japan",
        script=Script.SIDDHAM,
        description="Long text version. Reputedly brought to Japan from China "
                    "in 9th century by Yeun, disciple of Kūkai.",
        scholarly_refs=["Conze 1967"],
    ),

    # Nepalese witnesses
    "Na": Witness(
        id="Na",
        name="India Office no. 7712 (1)",
        witness_type=WitnessType.SANSKRIT,
        date="c. 18th century CE",
        date_circa=True,
        location="British Library (India Office Collection)",
        provenance="Nepal",
        script=Script.DEVANAGARI,
        description="Nepalese manuscript, relatively late.",
        scholarly_refs=["Conze 1967"],
    ),
    "Nb": Witness(
        id="Nb",
        name="Cambridge Add. 1485",
        witness_type=WitnessType.SANSKRIT,
        date="1677 CE",
        date_circa=False,
        location="Cambridge University Library",
        provenance="Nepal",
        material="Black paper with gold ink",
        script=Script.DEVANAGARI,  # Rañjana script
        description="Nepalese manuscript in Rañjana script. Gold ink on black paper. "
                    "Contains Prajñāpāramitāhṛdaya with other dhāraṇī texts (leaves 16-54).",
        scholarly_refs=["Conze 1967", "Bendall"],
    ),
    "Nc": Witness(
        id="Nc",
        name="MS Bodl. 1449 (59)",
        witness_type=WitnessType.SANSKRIT,
        date="1819 CE",
        date_circa=False,
        location="Bodleian Library, Oxford",
        provenance="Nepal",
        script=Script.DEVANAGARI,
        description="Nepalese manuscript, fol. 74v-75v.",
        scholarly_refs=["Conze 1967"],
    ),
    "Nd": Witness(
        id="Nd",
        name="Royal Asiatic Society no. 79 V",
        witness_type=WitnessType.SANSKRIT,
        date="c. 1820 CE",
        date_circa=True,
        location="Royal Asiatic Society, London",
        provenance="Nepal",
        script=Script.DEVANAGARI,
        description="Nepalese manuscript, fol. 15-16b.",
        scholarly_refs=["Conze 1967"],
    ),
    "Ne": Witness(
        id="Ne",
        name="Cambridge Add. 1553",
        witness_type=WitnessType.SANSKRIT,
        date="c. 18th century CE",
        date_circa=True,
        location="Cambridge University Library",
        provenance="Nepal",
        script=Script.DEVANAGARI,
        description="Nepalese manuscript, fol. 4-7b.",
        scholarly_refs=["Conze 1967"],
    ),
    "Nf": Witness(
        id="Nf",
        name="Asiatic Society of Bengal B 5 (35)",
        witness_type=WitnessType.SANSKRIT,
        date=None,
        location="Asiatic Society, Kolkata",
        provenance="Nepal",
        script=Script.DEVANAGARI,
        scholarly_refs=["Conze 1967"],
    ),
    "Ng": Witness(
        id="Ng",
        name="Asiatic Society of Bengal B 65 (10)",
        witness_type=WitnessType.SANSKRIT,
        date=None,
        location="Asiatic Society, Kolkata",
        provenance="Nepal",
        script=Script.DEVANAGARI,
        scholarly_refs=["Conze 1967"],
    ),
    "Nh": Witness(
        id="Nh",
        name="Cambridge Add. 1164.2 II",
        witness_type=WitnessType.SANSKRIT,
        date=None,
        location="Cambridge University Library",
        provenance="Nepal",
        script=Script.DEVANAGARI,
        description="Fragment - first 6 lines only. Same as Nl in Conze.",
        scholarly_refs=["Conze 1967"],
    ),
    "Ni": Witness(
        id="Ni",
        name="Société Asiatique no. 14",
        witness_type=WitnessType.SANSKRIT,
        date=None,
        location="Société Asiatique, Paris",
        provenance="Nepal",
        script=Script.DEVANAGARI,
        description="Nepalese manuscript, fol. 18b-19b. Long text version.",
        scholarly_refs=["Conze 1967"],
    ),
    "Nk": Witness(
        id="Nk",
        name="Cambridge Add. 1680 ix",
        witness_type=WitnessType.SANSKRIT,
        date="c. 1200 CE (13th century)",
        date_circa=True,
        location="Cambridge University Library",
        provenance="Nepal",
        material="Palm leaf",
        script=Script.DEVANAGARI,  # Bhujimol/Nepalese hooked script
        description="Section ix of bundle. Palm leaf in Bhujimol script. "
                    "Missing first leaf; begins at section 8. Worm damage. "
                    "One of the oldest Nepalese witnesses.",
        scholarly_refs=["Conze 1967", "Bendall"],
    ),

    # Chinese-provenance Sanskrit witnesses
    "Ca": Witness(
        id="Ca",
        name="Chinese blockprint",
        witness_type=WitnessType.SANSKRIT,
        date="c. 17th century CE",
        date_circa=True,
        provenance="China",
        script=Script.SIDDHAM,
        description="Sanskrit in Siddham script, Chinese blockprint.",
        scholarly_refs=["Conze 1967"],
    ),
    "Cb": Witness(
        id="Cb",
        name="Stein Collection Ch. S. 2464 (Sanskrit in Chinese characters)",
        witness_type=WitnessType.SANSKRIT,
        date="c. 600-700 CE",
        date_circa=True,
        location="British Library",
        provenance="Dunhuang",
        script=Script.TRADITIONAL_CHINESE,  # Sanskrit transliterated
        description="Sanskrit text transliterated into Chinese characters. "
                    "Corresponds to T256. Critical evidence for back-translation thesis.",
        scholarly_refs=["Conze 1967", "Nattier 1992"],
    ),
    "Cc": Witness(
        id="Cc",
        name="Mironov Mongolian Stone Inscription",
        witness_type=WitnessType.SANSKRIT,
        date="c. 10th-11th century CE",
        date_circa=True,
        location="Inner Mongolia",
        provenance="Mongolia",
        material="Stone",
        script=Script.SIDDHAM,
        description="Stone inscription from Inner Mongolia.",
        scholarly_refs=["Conze 1967", "Mironov"],
    ),
    "Cd": Witness(
        id="Cd",
        name="Mironov Bronze Bell Inscription",
        witness_type=WitnessType.SANSKRIT,
        date=None,
        location="Beijing",
        provenance="China",
        material="Bronze",
        script=Script.SIDDHAM,
        description="Inscription on bronze bell (~1.5m tall). Incomplete text.",
        scholarly_refs=["Conze 1967", "Mironov"],
    ),
    "Ce": Witness(
        id="Ce",
        name="Feer Polyglot Edition",
        witness_type=WitnessType.SANSKRIT,
        date="c. 17th century CE",
        date_circa=True,
        provenance="China → Japan",
        description="Historical polyglot edition (Sanskrit-Chinese-Japanese).",
        scholarly_refs=["Conze 1967", "Feer"],
    ),
    "Cf": Witness(
        id="Cf",
        name="Stein Collection Ch. 00330",
        witness_type=WitnessType.SANSKRIT,
        date="c. 850 CE",
        date_circa=True,
        location="British Library",
        provenance="Dunhuang",
        script=Script.SIDDHAM,
        scholarly_refs=["Conze 1967"],
    ),
    "Cg": Witness(
        id="Cg",
        name="Bibliothèque Nationale Pelliot Sogdien 62 no. 139",
        witness_type=WitnessType.SANSKRIT,
        date="c. 950 CE",
        date_circa=True,
        location="Bibliothèque Nationale de France, Paris",
        provenance="Central Asia (Dunhuang)",
        material="Birch bark",
        script=Script.SIDDHAM,
        description="Sogdian text on birch bark in Siddham script. "
                    "Same as Nm in some notation systems.",
        scholarly_refs=["Conze 1967"],
    ),

    # Gilgit manuscripts
    "Gilgit": Witness(
        id="Gilgit",
        name="Gilgit Manuscript Fragments",
        witness_type=WitnessType.SANSKRIT,
        date="c. 6th-7th century CE",
        date_circa=True,
        location="National Archives of India, New Delhi",
        provenance="Gilgit (modern Pakistan)",
        material="Birch bark",
        script=Script.DEVANAGARI,  # Proto-Śāradā
        description="Fragmentary. Covers approximately 80% of text. "
                    "Published by Raghu Vira and Lokesh Chandra (1966). "
                    "Important early witness.",
        scholarly_refs=["Raghu Vira & Lokesh Chandra 1966", "Karashima 2016"],
    ),
    # Parallel text (Large Prajñāpāramitā in Sanskrit)
    "Pancavimsati_Gilgit": Witness(
        id="Pancavimsati_Gilgit",
        name="Pañcaviṃśatisāhasrikā Prajñāpāramitā (Gilgit)",
        witness_type=WitnessType.PARALLEL,
        date="c. 7th century CE",
        date_circa=True,
        location="Various (fragments)",
        provenance="Gilgit",
        material="Birch bark",
        script=Script.DEVANAGARI,
        description="25,000 line PP. Sanskrit parallel for comparative analysis. "
                    "Contains the 'iha śāriputra...' passage paralleling Heart Sūtra core.",
        scholarly_refs=["Kimura", "Conze"],
    ),
}


# =============================================================================
# TIBETAN WITNESSES
# =============================================================================

TIBETAN_WITNESSES = {
    "Toh21": Witness(
        id="Toh21",
        name="Kangyur Toh 21 (Degé)",
        witness_type=WitnessType.TIBETAN,
        date="c. 9th century CE (translation)",
        date_circa=True,
        location="Degé Kangyur, Vol. 34, fol. 144b-146a",
        provenance="Tibet",
        script=Script.TIBETAN,
        description="Long version in Prajñāpāramitā section. "
                    "Translated by Vimalamitra and Rinchen Dé, "
                    "revised by Gewé Lodrö and Namkha.",
        scholarly_refs=["84000", "Silk 1994"],
    ),
    "Toh531": Witness(
        id="Toh531",
        name="Kangyur Toh 531 (Degé)",
        witness_type=WitnessType.TIBETAN,
        date="c. 9th century CE (translation)",
        date_circa=True,
        location="Degé Kangyur, Tantra section",
        provenance="Tibet",
        script=Script.TIBETAN,
        description="Alternative location in Tantra section.",
        scholarly_refs=["84000"],
    ),
    "Stok": Witness(
        id="Stok",
        name="Stok Palace Kangyur",
        witness_type=WitnessType.TIBETAN,
        date=None,
        location="Stok Palace, Ladakh",
        provenance="Tibet/Ladakh",
        script=Script.TIBETAN,
        description="Alternative recension (Recension B). Differs in title, "
                    "mantra rendering, and various phrasings.",
        scholarly_refs=["Silk 1994"],
    ),
    "IOL_Tib_J_751": Witness(
        id="IOL_Tib_J_751",
        name="IOL Tib J 751 (Dunhuang)",
        witness_type=WitnessType.TIBETAN,
        date="c. 823 CE",
        date_circa=True,
        location="British Library",
        provenance="Dunhuang",
        material="Paper",
        script=Script.TIBETAN,
        description="Late Old Tibetan version. Slightly differs from "
                    "both Kangyur versions and Sanskrit/Chinese texts.",
        scholarly_refs=["van Schaik"],
    ),
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_all_witnesses() -> dict[str, Witness]:
    """Return all witnesses combined."""
    all_witnesses = {}
    all_witnesses.update(CHINESE_WITNESSES)
    all_witnesses.update(SANSKRIT_WITNESSES)
    all_witnesses.update(TIBETAN_WITNESSES)
    return all_witnesses


def get_witnesses_by_type(witness_type: WitnessType) -> dict[str, Witness]:
    """Return witnesses of a specific type."""
    if witness_type == WitnessType.CHINESE:
        return CHINESE_WITNESSES
    elif witness_type == WitnessType.SANSKRIT:
        return SANSKRIT_WITNESSES
    elif witness_type == WitnessType.TIBETAN:
        return TIBETAN_WITNESSES
    elif witness_type == WitnessType.SOURCE:
        # Return source texts from all language collections
        return {k: v for k, v in get_all_witnesses().items()
                if v.witness_type == WitnessType.SOURCE}
    elif witness_type == WitnessType.PARALLEL:
        # Return parallel texts from all language collections
        return {k: v for k, v in get_all_witnesses().items()
                if v.witness_type == WitnessType.PARALLEL}
    return {}


def get_witness(siglum: str) -> Optional[Witness]:
    """Look up a witness by its siglum."""
    return get_all_witnesses().get(siglum)
