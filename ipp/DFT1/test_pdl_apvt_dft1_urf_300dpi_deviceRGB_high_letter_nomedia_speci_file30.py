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
    +external_files:printfile29.urf=776b25acdb482d1206f86be683ff25c5570c55232724a2e468a6509bf3c64b4c
    +test_classification:System
    +name:test_pdl_apvt_dft1_urf_300dpi_deviceRGB_High_letter_nomedia_speci_file30
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft1_urf_300dpi_deviceRGB_High_letter_nomedia_speci_file30
        +guid:01f6a12e-d8f8-4190-907f-7d76516e5bce
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & Certifications=AirPrint

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_apvt_dft1_urf_300dpi_deviceRGB_High_letter_nomedia_speci_file30(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw) 
    printjob.ipp_print_using_attribute_file('dft1_urf_300dpi_deviceRGB_High_letter_nomedia_speci_file30.test', '776b25acdb482d1206f86be683ff25c5570c55232724a2e468a6509bf3c64b4c')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"