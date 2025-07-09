import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite faces Page from *faces.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:200
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:faces.jpg=d625c95d10545cc5aa1e4ce2f276a7d423c1aa96a683a581a4bc243ee93393a2
    +test_classification:System
    +name:test_jpeg_testsuite_faces
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_faces
        +guid:a2736f04-acbf-47d5-b408-d5dcc794fc00
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testsuite_faces(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('d625c95d10545cc5aa1e4ce2f276a7d423c1aa96a683a581a4bc243ee93393a2', timeout=180)
    outputsaver.save_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    logging.info("JPEG TestSuite faces Page - Print job completed successfully")
