import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfilee15.urf=07154382c13947a5d97424f526cbe8b2ff2415384a39cf81efe07b5ee69327eb
    +test_classification:System
    +name:test_pdl_apvt_dft2_urf_300_duplex_RGB_letter_nomedia_speci_file16
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_urf_300_duplex_RGB_letter_nomedia_speci_file16
        +guid:8e00a0c3-5a63-42a3-aeb0-b277d98f2038
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=Canon & Print=Best & Certifications=AirPrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_urf_300_duplex_RGB_letter_nomedia_speci_file16(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_urf_300_duplex_RGB_letter_nomedia_speci_file16.test', '07154382c13947a5d97424f526cbe8b2ff2415384a39cf81efe07b5ee69327eb')
    outputsaver.save_output()