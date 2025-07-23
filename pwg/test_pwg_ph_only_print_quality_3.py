import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only print quality-3 page from *PwgPhOnly-PrintQuality-3.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-PrintQuality-3.pwg=ed10d043cbbe2cd301573d3c8c9cb508977de5d1421e18cbd6f46493c6c1fef0
    +name:test_pwg_ph_only_print_quality_3_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_print_quality_3_page
        +guid:a6b4c35b-7416-4d3f-90b5-a29732cf4ce5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_print_quality_3_page(setup_teardown, printjob,udw,outputsaver):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('ed10d043cbbe2cd301573d3c8c9cb508977de5d1421e18cbd6f46493c6c1fef0')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    logging.info("PWG Ph Only Print Quality-3 - Print job completed successfully")
