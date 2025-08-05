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
    +external_files:printfile29.urf=6c9b453c8d6d06a85393a41d9d2f984757ad676f4ae8a399d2ff524ada1204f9
    +test_classification:System
    +name:test_pdl_apvt_dft3_urf_300dpi_RGB_normal_nomedia_speci_file29
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft3_urf_300dpi_RGB_normal_nomedia_speci_file29
        +guid:485fb4e3-4a5c-4a7d-8c48-4df8d225d56c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in & Certifications=AirPrint

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft3_urf_300dpi_RGB_normal_nomedia_speci_file29(setup_teardown, printjob, outputsaver,tray,udw):
    outputsaver.validate_crc_tiff(udw)    
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')
    printjob.ipp_print_using_attribute_file('dft3_urf_300dpi_RGB_normal_nomedia_speci_file29.test', '6c9b453c8d6d06a85393a41d9d2f984757ad676f4ae8a399d2ff524ada1204f9')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

