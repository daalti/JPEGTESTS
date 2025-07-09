import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite combo aRGB embedded Page from *combo_aRGB_embedded.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:combo_aRGB_embedded.jpg=50f412884b1ddafb50dcadf66349776bbdcdbdcaa219cda6da5bb84f1e2e7cc6
    +test_classification:System
    +name:test_jpeg_testsuite_combo_aRGB_embedded
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_combo_aRGB_embedded
        +guid:c3ea2568-1453-4c59-af43-2cf3a6b8adc4
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testsuite_combo_aRGB_embedded(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('50f412884b1ddafb50dcadf66349776bbdcdbdcaa219cda6da5bb84f1e2e7cc6')
    outputsaver.save_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    logging.info("JPEG TestSuite combo aRGB embedded Page - Print job completed successfully")
