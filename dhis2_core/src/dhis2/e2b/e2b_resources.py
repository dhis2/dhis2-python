import logging
from datetime import datetime
from uuid import uuid4

from lxml import etree
from lxml.builder import E

from .common import (
    date_format_102,
    date_format_204,
    get_attribute_value,
    get_data_value,
    get_patient_age,
    get_patient_sex,
    get_reaction_outcome,
    get_yes_no,
)
from .models.e2b import Enrollment, TrackedEntity

log = logging.getLogger(__name__)


def build_messageheader(root: etree.Element):
    mh = E.ichicsrmessageheader(
        E.messagetype("ichicsr"),
        E.messageformatversion("2.1"),
        E.messageformatrelease("2.0"),
        E.messagenumb(str(uuid4())),
        E.messagesenderidentifier("REPLACE_ME"),
        E.messagereceiveridentifier("REPLACE_ME"),
        E.messagedateformat("204"),
        E.messagedate(date_format_204(datetime.now())),
    )

    root.append(mh)


def build_safetyreport_patient_drug(
    root: etree.Element,
    name: str,
    date: str,
    time: str,
    batch: str,
    dose: str,
    diluent_name: str,
    diluent_batch: str,
    diluent_expiry: str,
    diluent_dor: str,
    diluent_tor: str,
):
    dt = datetime.fromisoformat(f"{date}T{time}")

    drug = etree.SubElement(root, "drug")
    drug.append(E.drugcharacterization("2"))
    drug.append(E.medicinalproduct(name))
    drug.append(E.drugstartdateformat("204"))
    drug.append(E.drugstartdate(date_format_204(dt)))
    drug.append(E.drugenddateformat("204"))
    drug.append(E.drugenddate(date_format_204(dt)))

    if dose:
        drug.append(E.drugstructuredosagenumb(dose))

    drug.append(E.drugbatchnumb(batch))

    dilutent = []

    if diluent_name:
        dilutent.append(f"Name of diluent: {diluent_name}")

    if diluent_batch:
        dilutent.append(f"Dilutent batch/lot number: {diluent_batch}")

    if diluent_expiry:
        dilutent.append(f"Dilutent expiry date: {diluent_expiry}")

    if diluent_dor:
        dilutent.append(f"Dilutent date of reconstitution: {diluent_dor}")

    if diluent_tor:
        dilutent.append(f"Dilutent time of reconstitution: {diluent_tor}")

    if dilutent:
        drug.append(E.drugadditional(", ".join(dilutent)))


def build_safetyreport_patient_drugs(root: etree.Element, te: TrackedEntity):
    vaccine1_name = get_data_value("uSVcZzSM3zg", te)
    vaccine1_date = get_data_value("dOkuCjpD978", te)
    vaccine1_time = get_data_value("BSUncNBb20j", te)
    vaccine1_batch = get_data_value("LNqkAlvGplL", te)
    vaccine1_dose = get_data_value("LIyV4t7eCfZ", te)
    vaccine2_name = get_data_value("g9PjywVj2fs", te)
    vaccine2_date = get_data_value("VrzEutEnzSJ", te)
    vaccine2_time = get_data_value("fZFQVZFqu0q", te)
    vaccine2_batch = get_data_value("b1rSwGRcY5W", te)
    vaccine2_dose = get_data_value("E3F414izniN", te)
    vaccine3_name = get_data_value("OU5klvkk3SM", te)
    vaccine3_date = get_data_value("f4WCAVwjHz0", te)
    vaccine3_time = get_data_value("VQKdZ1KeD7u", te)
    vaccine3_batch = get_data_value("YBnFoNouH6f", te)
    vaccine3_dose = get_data_value("WlE0K4xCc14", te)
    vaccine4_name = get_data_value("menOXwIFZh5", te)
    vaccine4_date = get_data_value("H3TKHMFIN6V", te)
    vaccine4_time = get_data_value("S1PRFSk8Y9v", te)
    vaccine4_batch = get_data_value("BHAfwo6JPDa", te)
    vaccine4_dose = get_data_value("Aya8C25DXHe", te)

    diluent1_name = get_data_value("xk9QvZPMVQF", te)
    diluent1_batch = get_data_value("FQM2ksIQix8", te)
    diluent1_expiry = get_data_value("cKx0VCmLrsc", te)
    diluent1_dor = get_data_value("om7AsREDduc", te)  # Date of reconstitution
    diluent1_tor = get_data_value("zIKVrYHtdUx", te)  # Time of reconstitution
    diluent2_name = get_data_value("WN8844HG0zi", te)
    diluent2_batch = get_data_value("ufWU3WStZgG", te)
    diluent2_expiry = get_data_value("FcqNLPNUPId", te)
    diluent2_dor = get_data_value("xXjnT9sjt4F", te)  # Date of reconstitution
    diluent2_tor = get_data_value("KTHsZhIAGWf", te)  # Time of reconstitution
    diluent3_name = get_data_value("pLu0luPWikb", te)
    diluent3_batch = get_data_value("MLP8fi1X7UX", te)
    diluent3_expiry = get_data_value("MGjnXmtmd7l", te)
    diluent3_dor = get_data_value("fW6RbpJk4hS", te)  # Date of reconstitution
    diluent3_tor = get_data_value("gG0FZYpEctJ", te)  # Time of reconstitution
    diluent4_name = get_data_value("ZTyN8vSf7bc", te)
    diluent4_batch = get_data_value("MyWtDaOdlyD", te)
    diluent4_expiry = get_data_value("qhDonTAIjl0", te)
    diluent4_dor = get_data_value("va0Smpy0LUn", te)  # Date of reconstitution
    diluent4_tor = get_data_value("EDdd0HsfLcO", te)  # Time of reconstitution

    if vaccine1_name:
        build_safetyreport_patient_drug(
            root,
            name=vaccine1_name,
            date=vaccine1_date,
            time=vaccine1_time,
            batch=vaccine1_batch,
            dose=vaccine1_dose,
            diluent_name=diluent1_name,
            diluent_batch=diluent1_batch,
            diluent_expiry=diluent1_expiry,
            diluent_dor=diluent1_dor,
            diluent_tor=diluent1_tor,
        )

    if vaccine2_name:
        build_safetyreport_patient_drug(
            root,
            name=vaccine2_name,
            date=vaccine2_date,
            time=vaccine2_time,
            batch=vaccine2_batch,
            dose=vaccine2_dose,
            diluent_name=diluent2_name,
            diluent_batch=diluent2_batch,
            diluent_expiry=diluent2_expiry,
            diluent_dor=diluent2_dor,
            diluent_tor=diluent2_tor,
        )

    if vaccine3_name:
        build_safetyreport_patient_drug(
            root,
            name=vaccine3_name,
            date=vaccine3_date,
            time=vaccine3_time,
            batch=vaccine3_batch,
            dose=vaccine3_dose,
            diluent_name=diluent3_name,
            diluent_batch=diluent3_batch,
            diluent_expiry=diluent3_expiry,
            diluent_dor=diluent3_dor,
            diluent_tor=diluent3_tor,
        )

    if vaccine4_name:
        build_safetyreport_patient_drug(
            root,
            name=vaccine4_name,
            date=vaccine4_date,
            time=vaccine4_time,
            batch=vaccine4_batch,
            dose=vaccine4_dose,
            diluent_name=diluent4_name,
            diluent_batch=diluent4_batch,
            diluent_expiry=diluent4_expiry,
            diluent_dor=diluent4_dor,
            diluent_tor=diluent4_tor,
        )


def build_safetyreport_patient_reactions(root: etree.Element, te: TrackedEntity):
    p = etree.SubElement(root, "reaction")
    outcome = get_reaction_outcome(te)
    startdate = get_data_value("vNGUuAZA2C2", te)

    severe_local_reaction = get_data_value("UNmEidE6M9K", te)
    severe_above_3_days = get_data_value("We87rvcvd8J", te)
    severe_beyond_nearest_joint = get_data_value("f8hjxmHOtAB", te)
    seizures = get_data_value("wCGZpudXuYx", te)
    seizures_type = get_data_value("Zz4KYO4AsSY", te)
    abscess = get_data_value("wce39JmsjIK", te)
    sepsis = get_data_value("tUmgO1Ugv6U", te)
    encephalopathy = get_data_value("pdpAEuUS1W9", te)
    toxic_shock_syndrome = get_data_value("Apq4JaueuWR", te)
    thrombocytopenia = get_data_value("GGLLaieVChK", te)
    anaphylaxis = get_data_value("MkIgCrCTFyE", te)
    fever_above_38 = get_data_value("rzhHSqK3lQq", te)

    if outcome:
        p.append(E.reactionoutcome(outcome))

    if startdate:
        datetime_startdate = datetime.fromisoformat(startdate)
        p.append(E.reactionstartdateformat("102"))
        p.append(E.reactionstartdate(date_format_102(datetime_startdate)))

    primarysourcereaction = []

    if severe_local_reaction:
        primarysourcereaction.append("Severe local reaction")

        if severe_above_3_days:
            primarysourcereaction.append(">3 days")

        if severe_beyond_nearest_joint:
            primarysourcereaction.append("Beyond nearest joint")

    if seizures:
        if seizures_type:
            primarysourcereaction.append(f"Seizures ({seizures_type})")
        else:
            primarysourcereaction.append("Seizures")

    if abscess:
        primarysourcereaction.append("Abscess")

    if sepsis:
        primarysourcereaction.append("Sepsis")

    if encephalopathy:
        primarysourcereaction.append("Encephalopathy")

    if toxic_shock_syndrome:
        primarysourcereaction.append("Toxic shock syndrome")

    if thrombocytopenia:
        primarysourcereaction.append("Thrombocytopenia")

    if anaphylaxis:
        primarysourcereaction.append("Anaphylaxis")

    if fever_above_38:
        primarysourcereaction.append("Fever (> 38°C)")

    if primarysourcereaction:
        p.append(E.primarysourcereaction(", ".join(primarysourcereaction)))


def build_safetyreport_patient(root: etree.Element, te: TrackedEntity):
    p = etree.SubElement(root, "patient")

    p.append(E.patientinitial(get_attribute_value("TfdH5KvFmMy", te)))  # should we use name here or not?
    p.append(E.patientonsetage(get_patient_age(te)))
    p.append(E.patientonsetageunit("801"))
    p.append(E.patientsex(get_patient_sex(te)))

    if get_yes_no("VXdRoWQOBxG", te):
        p.append(
            E.medicalhistoryepisode(
                E.patientmedicalcomment(get_data_value("AfrWB2ofm7l", te) or ""),
            )
        )

    p.append(
        E.summary(
            E.reportercomment(get_data_value("IV9W7YXh939", te)),
        )
    )

    build_safetyreport_patient_drugs(p, te)
    build_safetyreport_patient_reactions(p, te)


def build_safetyreport(root: etree.Element, te: TrackedEntity, en: Enrollment):
    sr = etree.SubElement(root, "safetyreport")

    sr.append(E.safetyreportversion("1"))
    sr.append(E.safetyreportid(str(uuid4())))
    sr.append(E.primarysourcecountry("REPLACE_ME"))
    sr.append(E.occurcountry("REPLACE_ME"))
    sr.append(E.transmissiondateformat("102"))
    sr.append(E.transmissiondate(date_format_102(datetime.now())))
    sr.append(E.reporttype("1"))
    sr.append(E.serious(get_yes_no("fq1c1A3EOX5", te)))

    dead = get_yes_no("DOA6ZFMro84", te) == "1"

    if dead:
        date_of_death = get_data_value("Ze34uXcBUxi", te)
        autopsyyesno = get_data_value("yRrSDiR5v1M", te) == "Autopsy done"

        if autopsyyesno:
            autopsyyesno = "1"
        else:
            autopsyyesno = "2"

        datetime_of_death = None

        if date_of_death:
            datetime_of_death = datetime.fromisoformat(date_of_death)

        sr.append(E.seriousnessdeath("1"))

        if datetime_of_death:
            sr.append(
                E.patientdeath(
                    E.patientdeathdateformat("102"),
                    E.patientdeathdate(date_format_102(datetime_of_death)),
                    E.patientautopsyyesno(autopsyyesno),
                )
            )
    else:
        sr.append(E.seriousnessdeath("2"))

    sr.append(E.seriousnesslifethreatening(get_yes_no("lATDYNmTLKD", te)))
    sr.append(E.seriousnesshospitalization(get_yes_no("Il1lTfknLdd", te)))
    sr.append(E.seriousnessdisabling(get_yes_no("lsO8n8ZmLAB", te)))
    sr.append(E.seriousnesscongenitalanomali(get_yes_no("lSBsxcQU0kO", te)))
    sr.append(E.seriousnessother(get_yes_no("tWcNgbkOETR", te)))
    sr.append(E.receivedateformat("102"))
    sr.append(E.receivedate(date_format_102(datetime.now())))
    sr.append(E.receiptdateformat("102"))
    sr.append(E.receiptdate(date_format_102(datetime.now())))
    sr.append(E.additionaldocument("2"))
    sr.append(E.fulfillexpeditecriteria("1"))
    sr.append(E.authoritynumb(get_attribute_value("h5FuguPFF2j", te)))

    sr.append(
        E.primarysource(
            E.reportergivename(get_data_value("uZ9c4fKXuNS", te)),
        )
    )

    sr.append(
        E.sender(
            E.senderorganization(get_data_value("Q20pEixZxCs", te)),  # TODO resolve org unit
            E.senderdepartment(get_data_value("Tgi4xP5DCzr", te)),
        )
    )

    sr.append(
        E.receiver(
            E.receivertype("5"),
            E.receiverorganization("WHO"),
            E.receivercountrycode("ch"),
        )
    )

    build_safetyreport_patient(sr, te)


def print_root(root: etree.Element, pretty_print: bool = True):
    print(
        etree.tostring(
            root,
            pretty_print=pretty_print,
            standalone=True,
            encoding="UTF-8",
            doctype='<!DOCTYPE ichicsr SYSTEM "http://eudravigilance.ema.europa.eu/dtd/icsr21xml.dtd">',
        ).decode()
    )
