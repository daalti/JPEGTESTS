import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile3.urf=227884b787d83496883d48de265732e6a013360cd86d5fbfd7f26d9ec164454b
    +test_classification:System
    +name:test_pdl_apvt_dft4_urf_600dpi_deviceRGB_roll_auto_file3
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft4_urf_600dpi_deviceRGB_roll_auto_file3
        +guid:ff570b70-5c89-46dd-a3ec-2fbc091c7d65
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & MediaInputInstalled=MainRoll & Certifications=AirPrint

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_apvt_dft4_urf_600dpi_deviceRGB_roll_auto_file3(setup_teardown, printjob, outputsaver,udw):
    printjob.ipp_print_using_attribute_file('dft4_urf_600dpi_deviceRGB_roll_auto_file3.test', '227884b787d83496883d48de265732e6a013360cd86d5fbfd7f26d9ec164454b')
    outputsaver.save_output()
    
    # CRC check
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')