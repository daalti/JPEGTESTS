import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Print PCL5 font list in French
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-5484
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +name:test_pcl5FontList_in_french
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5FontList_in_french
        +guid:438a64e3-13e1-49f2-bf93-21dd6002776c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5 & Language=fr-FR & ConsumableSupport=Toner
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5FontList_in_french(setup_teardown, printjob, outputverifier, outputsaver, udw, cdm):

    outputsaver.validate_crc_tiff(udw)
    
    configuration_endpoint = cdm.SYSTEM_CONFIGURATION
    cdmvalue = cdm.get(configuration_endpoint)
    logging.info("By default english language is selected")
    logging.info(cdmvalue["deviceLanguage"])
    
    #setting the language to French
    cdm.device_language.set_device_language("fr")

    cdmvalue = cdm.get(configuration_endpoint)
    logging.info("french language is selected")
    logging.info(cdmvalue["deviceLanguage"])

    assert cdmvalue["deviceLanguage"] == "fr"

    reports = printjob.get_printer_reports()
    report_id = 'pclFontList'
    reports = [report for report in reports if report.get('reportId') == report_id]
    assert len(reports) > 0, 'no reports with the given reportId'

    printjob.bookmark_jobs()

    logging.info('Printing Internal Report: %s', reports[0]['localizedName'])
    response = cdm.patch_raw(
        endpoint='/cdm/report/v1/print',
        json={
            'reportId': reports[0]['reportId'],
            'state': 'processing'
        })
    status = response.status_code

    assert status == 204, "status=%d" % status

    job_ids = printjob.wait_for_jobs(restricted_jobs_only=False)
    job_id = job_ids[-1]

    printjob.wait_verify_job_completion(job_id, 'SUCCESS')

    outputverifier.save_and_parse_output()

    Current_crc_value = outputsaver.get_crc()
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

