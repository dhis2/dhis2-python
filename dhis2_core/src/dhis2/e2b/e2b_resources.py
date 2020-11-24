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

    if vaccine1_name:
        build_safetyreport_patient_drug(
            root,
            name=vaccine1_name,
            date=vaccine1_date,
            time=vaccine1_time,
            batch=vaccine1_batch,
            dose=vaccine1_dose,
        )

    if vaccine2_name:
        build_safetyreport_patient_drug(
            root,
            name=vaccine2_name,
            date=vaccine2_date,
            time=vaccine2_time,
            batch=vaccine2_batch,
            dose=vaccine2_dose,
        )

    if vaccine3_name:
        build_safetyreport_patient_drug(
            root,
            name=vaccine3_name,
            date=vaccine3_date,
            time=vaccine3_time,
            batch=vaccine3_batch,
            dose=vaccine3_dose,
        )

    if vaccine4_name:
        build_safetyreport_patient_drug(
            root,
            name=vaccine4_name,
            date=vaccine4_date,
            time=vaccine4_time,
            batch=vaccine4_batch,
            dose=vaccine4_dose,
        )


def build_safetyreport_patient_reactions(root: etree.Element, te: TrackedEntity):
    pass


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
        datetime_of_death = None

        if date_of_death:
            datetime_of_death = datetime.fromisoformat(date_of_death)

        sr.append(E.seriousnessdeath("1"))

        if datetime_of_death:
            sr.append(
                E.patientdeath(
                    E.patientdeathdateformat("102"),
                    E.patientdeathdate(date_format_102(datetime_of_death)),
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
