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
    +external_files:printfile42.urf=5e5e3ea266f38cf84c1d6c5ea8809b858a3e3aa5254ee40a9cb70377ecf0bbb9
    +test_classification:System
    +name:test_pdl_apvt_dft1_urf_mixedpageurf_deviceRGB_devicegray_letter_nomedia_speci_file42
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft1_urf_mixedpageurf_deviceRGB_devicegray_letter_nomedia_speci_file42
        +guid:c0c7a5e8-166b-4eb2-977e-2a31d037466b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & Certifications=AirPrint

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_apvt_dft1_urf_mixedpageurf_deviceRGB_devicegray_letter_nomedia_speci_file42(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft1_urf_mixedpageurf_deviceRGB_devicegray_letter_nomedia_speci_file42.test', '5e5e3ea266f38cf84c1d6c5ea8809b858a3e3aa5254ee40a9cb70377ecf0bbb9')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"