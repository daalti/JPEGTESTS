import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Raw text data via PCL5 **Raw_text.txt
    +test_tier: 1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-202711
    +timeout:360
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Raw_text.txt=32012442531e0b9ebc4578d2af60c2a97958fe4d38df9d4c53506ea902290cac
    +name:test_pcl5_basicfunctionality_raw_text
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_basicfunctionality_raw_text
        +guid:50d5a02b-2acd-411a-9c11-ed9bab4b7144
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_raw_text(setup_teardown, printjob, outputverifier, outputsaver, udw):
    if outputsaver.is_pdl_supported('PCL'):
        outputsaver.validate_crc_tiff(udw)
        printjob.print_verify('32012442531e0b9ebc4578d2af60c2a97958fe4d38df9d4c53506ea902290cac')
        outputsaver.save_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    else:
        printjob.print_verify('32012442531e0b9ebc4578d2af60c2a97958fe4d38df9d4c53506ea902290cac', 'FAILED')