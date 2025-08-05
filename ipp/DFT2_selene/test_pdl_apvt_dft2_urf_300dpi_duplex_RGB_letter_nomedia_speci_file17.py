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
    +external_files:Printfile17.urf=347922a1e8349d1f46cba2388b9042d07e7051599d41fc241865d99001049439
    +test_classification:System
    +name:test_pdl_apvt_dft2_urf_300_duplex_RGB_letter_nomedia_speci_file17
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_urf_300_duplex_RGB_letter_nomedia_speci_file17
        +guid:a1100e1f-a20a-4f76-8e6e-132ed321fdb1
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=Canon & Certifications=AirPrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_urf_300_duplex_RGB_letter_nomedia_speci_file17(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_urf_300_duplex_RGB_letter_nomedia_speci_file17.test', '347922a1e8349d1f46cba2388b9042d07e7051599d41fc241865d99001049439')
    outputsaver.save_output()