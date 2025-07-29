import pytest
import logging
import time
import requests

from dunetuf.localization.LocalizationHelper import LocalizationHelper
from tests.print.lib.actions.print_helper import Print



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of packets_cmyk_planar_2_colors.rs and pause job
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18107
    +timeout:600
    +asset:LFP
    +test_framework:TUF
    +delivery_team:LFP
    +feature_team:ProductQA
    +external_files:packets_cmyk_planar_2_colors.rs=85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8
    +test_classification:System
    +name:test_rs_packets_cmyk_planar_2_colors_pause_job
    +test:
        +title:test_rs_packets_cmyk_planar_2_colors_pause_job
        +guid:82a1060e-e478-11eb-b72f-1310a3a83cad
        +dut:
            +type:Emulator
            +configuration: DocumentFormat=RasterStreamPlanarICF & PrintEngineType=MaiaLatex
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_packets_cmyk_planar_2_colors_pause_job(setup_teardown, printjob, job, tclMaia, spice, net, locale: str = "en-US"):

    # start printing and stop the job
    helper = Print(printjob, job, tclMaia)

    job_id = helper.print_and_stop("85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8")

    # check alert screen
    alert_image = spice.wait_for("#TitleText SpiceLottieImageView")
    assert str(alert_image["source"]) == str("qrc:/images/Status/ErrorFill.json")

    alert_description = spice.wait_for("#alertDetailDescription SpiceText[visible=true]")
    assert str(LocalizationHelper.get_string_translation(net, "cClosePrintZoneWindow", locale)) == str(alert_description["text"])

    time.sleep(10)
    # close the cover
    tclMaia.execute("WindowSensor setValue 0")

    # check job is finished
    printjob.wait_for_job_completion(job_id, timeout=600)


@pytest.fixture(autouse=True)
def setup_teardown(job, outputsaver, device, media, tclMaia):
    """Default setup/teardown fixture for Print tests."""
    logging.info('-- SETUP (Print Tests) --')

    result = device.device_ready(150)
    logging.info('Device Status: %s', result)
    assert all(result.values()), "Device not in ready state!"

    # ---- Setup Maia Ready ----
    try:
        tclMaia.execute("setEmulatorReady", recvTimeout=20)
    except ConnectionRefusedError:
        logging.info('The setEmulatorReady command not supported!')

    job.cancel_active_jobs()
    outputsaver.clear_output()

    yield

    logging.info('-- TEARDOWN (Print Tests) --')
    time.sleep(10)

    try:
        tclMaia.execute("WindowSensor setValue 0")
        media.get_alerts()
    except requests.exceptions.HTTPError:
        logging.warning('The CDM endpoint "/cdm/mediaHandling/v1/alerts" is not supported!')

    outputsaver.clear_output()
    job.cancel_active_jobs()

    
