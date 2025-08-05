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
    +external_files:printfile25.urf=130691bf2d8bddc2853f06503ebfcd5a44dc23f41aea614e68099887a63430ce
    +test_classification:System
    +name:test_pdl_apvt_dft3_urf_300dpi_Gray_nomedia_speci_file26
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft3_urf_300dpi_Gray_nomedia_speci_file26
        +guid:116131fc-880a-43c5-aafd-518ca703b69a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in & Certifications=AirPrint

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft3_urf_300dpi_Gray_nomedia_speci_file26(setup_teardown, printjob, outputsaver,tray,udw):
    outputsaver.validate_crc_tiff(udw)    
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')
    printjob.ipp_print_using_attribute_file('dft3_urf_300dpi_Gray_nomedia_speci_file26.test', '130691bf2d8bddc2853f06503ebfcd5a44dc23f41aea614e68099887a63430ce')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

