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
    +external_files:printfile52.urf=5f9bdfe8d3f056ee3d15109f57664d3edc4da109637b72110de10378451ead12
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_urf_duplex_150dpi_deviceGray_normal_auto_file53
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_urf_duplex_150dpi_deviceGray_normal_auto_file53
        +guid:f07c27ad-2773-4f3a-9a07-847a0571d8c2
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=JPEG & PrintProtocols=IPP & ConsumableSupport=Ink&MediaInputInstalled=Tray1 & Certifications=AirPrint

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_urf_duplex_150dpi_deviceGray_normal_auto_file53(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft2_dox_urf_duplex_150dpi_deviceGray_normal_auto_file53.test', '5f9bdfe8d3f056ee3d15109f57664d3edc4da109637b72110de10378451ead12')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    # tray.reset_trays()

    logging.info("Print job completed successfully")