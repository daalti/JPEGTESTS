import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite combo SWOP embedded Page from *combo_SWOP_embedded.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:combo_SWOP_embedded.jpg=d9904a956bcf378816ff4f2c5c7ef8c6b8e03a68f7bcdad1aa0a47f218508b88
    +test_classification:System
    +name:test_jpeg_testsuite_combo_SWOP_embedded
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_combo_SWOP_embedded
        +guid:b60d4338-2f28-4c3d-acba-ce5c8511955f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testsuite_combo_SWOP_embedded(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('d9904a956bcf378816ff4f2c5c7ef8c6b8e03a68f7bcdad1aa0a47f218508b88')
    outputsaver.save_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    logging.info("JPEG TestSuite combo SWOP embedded Page - Print job completed successfully")
