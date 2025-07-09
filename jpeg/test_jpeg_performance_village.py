import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52178012 Simple print job of Jpeg Performance of village Page from *village.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:village.jpg=ff0629b82de8d14c732795720966dfa96a8c8231553415c175af735ce47a0ef5
    +test_classification:System
    +name:test_jpeg_performance_village
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_performance_village
        +guid:aac778c3-62d9-425f-8b7e-32316e4d0fad
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_performance_village(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('ff0629b82de8d14c732795720966dfa96a8c8231553415c175af735ce47a0ef5')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc() 
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    logging.info("JPEG Performance village Page - Print job completed successfully")
