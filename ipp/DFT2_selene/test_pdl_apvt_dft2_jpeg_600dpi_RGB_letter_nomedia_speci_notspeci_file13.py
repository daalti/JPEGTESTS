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
    +external_files:printfile13.urf=14a640a6f850a27a0ef27ee300a182e9fdc8703de54755705e15df139df21a88
    +test_classification:System
    +name:test_pdl_apvt_dft2_urf_600dpi_RGB_letter_nomedia_speci_notspeci_file13
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_urf_600dpi_RGB_letter_nomedia_speci_notspeci_file13
        +guid:0e8f92ce-d936-441b-a01c-32c51a82b6d3
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=JPEG & PrintProtocols=IPP & EngineFirmwareFamily=Canon & Print=Best & Certifications=AirPrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_urf_600dpi_RGB_letter_nomedia_speci_notspeci_file13(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_urf_600dpi_RGB_letter_nomedia_speci_notspeci_file13.test', '14a640a6f850a27a0ef27ee300a182e9fdc8703de54755705e15df139df21a88')
    outputsaver.save_output()