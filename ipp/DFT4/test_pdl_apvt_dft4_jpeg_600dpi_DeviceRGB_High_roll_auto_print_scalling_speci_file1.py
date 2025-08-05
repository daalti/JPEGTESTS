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
    +external_files:printfile1.jpg=e8cfa9196d978ce47436f30d3b89ba21ffd05e9f3a4dd2048d0e42b5c86b13a2
    +test_classification:System
    +name:test_pdl_apvt_dft4_jpeg_600dpi_DeviceRGB_High_roll_auto_print_scalling_speci_file1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft4_jpeg_600dpi_DeviceRGB_High_roll_auto_print_scalling_speci_file1
        +guid:44a1ad6b-b0dc-4148-a9d9-fcf7943e2df5
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=JPEG & PrintProtocols=IPP & MediaInputInstalled=MainRoll
 & Certifications=AirPrint

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_apvt_dft4_jpeg_600dpi_DeviceRGB_High_roll_auto_print_scalling_speci_file1(setup_teardown, printjob, outputsaver, udw):
    printjob.ipp_print_using_attribute_file('dft4_jpeg_600dpi_DeviceRGB_High_roll_auto_print_scalling_speci_file1.test', 'e8cfa9196d978ce47436f30d3b89ba21ffd05e9f3a4dd2048d0e42b5c86b13a2')
    outputsaver.save_output()
    
    # CRC check
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')